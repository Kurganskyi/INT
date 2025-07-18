"""
validate_result.py — Валидация XML по XSD с анализом ошибок

Назначение:
    Скрипт предназначен для автоматической валидации XML-файла по XSD-схеме с учётом всех импортируемых схем, а также для подробного анализа ошибок валидации. Для каждой ошибки формируется человекочитаемый отчёт с указанием, что именно не совпадает с эталонным примером.

Логика работы:
1. Загрузка схемы XSD
   - Основная схема (MZAZ_2024-01-01.xsd) загружается с помощью библиотеки xmlschema, которая автоматически подгружает все связанные схемы через <xs:import>.
   - В случае ошибки парсинга схемы скрипт завершает работу и пишет ошибку в файл.
2. Валидация XML
   - Проверяется файл Результат.txt на соответствие XSD.
   - Все ошибки валидации собираются в список.
3. Анализ ошибок
   - Для каждой ошибки определяется XPath к проблемному элементу.
   - Из файла результата (Результат.txt) и эталонного файла (example_result.xml) извлекаются значения по этому XPath с учётом пространств имён.
   - Формируется подробное сообщение:
     Ошибка N - <Имя_атрибута> "фактическое_значение" <.Имя_атрибута>, а должно быть <Имя_атрибута> "значение_из_эталона" <.Имя_атрибута>
   - Между ошибками добавляется пустая строка для удобства чтения.
4. Итог
   - В конце отчёта указывается общее количество ошибок.
   - Все сообщения сохраняются в файл validation_errors.txt.

Применение:
    Скрипт помогает быстро выявить и локализовать расхождения между сгенерированным XML и эталонным примером.
    Удобен для отладки шаблонов генерации XML, интеграции с CI/CD, автоматизации тестирования.

Требования:
    Python 3.7+
    Библиотеки: xmlschema

Запуск:
    python validate_result.py
"""

import xmlschema
import sys
import os
import xml.etree.ElementTree as ET

xml_file = "Результат.txt"
xsd_file = os.path.join("..", "valid", "MZAZ_2024-01-01.xsd")
example_file = "example_result.xml"
error_path = os.path.join(os.path.dirname(__file__), "validation_errors.txt")

# Получить словарь пространств имён из XML
def get_namespaces(xml_path):
    events = "start", "start-ns"
    ns_map = {}
    for event, elem in ET.iterparse(xml_path, events):
        if event == "start-ns":
            prefix, uri = elem
            ns_map[prefix if prefix is not None else ''] = uri
    return ns_map

# Найти значение по XPath с учётом namespace
def find_value_by_xpath(xml_path, xpath, nsmap):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # Преобразуем путь ошибки в XPath для ElementTree
        # /ЭДСФР/МЗАЗ/Заявитель/УТ7:Код -> .//{uri}Код
        parts = xpath.strip('/').split('/')
        current = root
        for part in parts[1:]:  # пропускаем корень
            if ':' in part:
                prefix, tag = part.split(':')
                uri = nsmap.get(prefix, '')
                search = f'{{{uri}}}{tag}'
            else:
                uri = nsmap.get('', '')
                search = f'{{{uri}}}{part}' if uri else part
            found = current.find(search)
            if found is None:
                return None
            current = found
        return current.text.strip() if current.text else None
    except Exception:
        return None

errors = []
try:
    schema = xmlschema.XMLSchema(xsd_file)
except Exception as e:
    msg = f"Ошибка при парсинге XSD: {e}"
    print(msg)
    errors.append(msg)
    with open(error_path, "w", encoding="utf-8") as f:
        f.write("\n".join(errors))
    print(f"Все ошибки сохранены в {error_path}")
    sys.exit(1)

# Получаем nsmap для эталона и результата
example_nsmap = get_namespaces(example_file)
result_nsmap = get_namespaces(xml_file)

try:
    validation_errors = list(schema.iter_errors(xml_file))
    if not validation_errors:
        print("XML валиден по XSD!")
    else:
        print("XML НЕ валиден по XSD!")
        for idx, error in enumerate(validation_errors, 1):
            path = error.path or error.elem_path or ''
            attr = path.split('/')[-1] if path else 'Неизвестно'
            # Фактическое значение из результата
            fact = find_value_by_xpath(xml_file, path, result_nsmap)
            # Ожидаемое значение из примера
            example = find_value_by_xpath(example_file, path, example_nsmap)
            msg = f'Ошибка {idx} - <{attr}> "{fact if fact is not None else "(нет данных)"}" <.{attr}>, а должно быть <{attr}> "{example if example is not None else "(нет данных)"}" <.{attr}>'
            print(msg)
            errors.append(msg)
            errors.append("")  # пустая строка между ошибками
        errors.append(f'Итого ошибок: {len(validation_errors)}')
finally:
    if errors:
        with open(error_path, "w", encoding="utf-8") as f:
            f.write("\n".join(errors))
        print(f"Все ошибки сохранены в {error_path}") 