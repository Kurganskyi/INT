import re
import os
import json
from xml.dom.minidom import parseString

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TASKS = [
    ('form1', 'process_form1.xml'),
    ('form2', 'process_form2.xml'),
]

XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>\n'

for folder, out_name in TASKS:
    input_path = os.path.join(BASE_DIR, folder, 'export_task')
    output_path = os.path.join(BASE_DIR, out_name)
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = f.read()
        match = re.search(r'"RawValue"\s*:\s*"(.*?)"\s*,\s*\n', data, re.DOTALL)
        if not match:
            print(f'RawValue не найден в {input_path}!')
            continue
        raw_value_escaped = match.group(1)
        xml = json.loads(f'"{raw_value_escaped}"')
        # Форматируем XML с отступами
        xml_str = xml.lstrip()
        if not xml_str.startswith('<?xml'):
            xml_str = XML_DECLARATION + xml_str
        # minidom pretty print
        dom = parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="    ", encoding="utf-8").decode("utf-8")
        # Удаляем пустые строки, которые добавляет minidom
        pretty_xml = '\n'.join([line for line in pretty_xml.splitlines() if line.strip()])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        print(f'XML из {input_path} успешно извлечён и сохранён в {output_path}')
    except Exception as e:
        print(f'Ошибка при обработке {input_path}: {e}')

input('Нажмите Enter для выхода...')