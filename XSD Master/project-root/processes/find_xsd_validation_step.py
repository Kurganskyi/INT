import xml.etree.ElementTree as ET
import argparse
import sys

# Для pretty-print
import xml.dom.minidom

def find_xsd_validation_step(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # Ищем шаг с валидацией по xsd (по тегу, содержащему 'Validation' или namespace SendSoap)
    for step in root.findall('.//{*}Step'):
        # Проверяем наличие тегов, связанных с xsd валидацией
        for child in step:
            # Обычно это что-то вроде <Data ... xsi:type="st:SoapXsdValidationData">
            if child.tag.endswith('Data') and 'xsi:type' in child.attrib:
                if 'Validation' in child.attrib['xsi:type'] or 'XsdValidation' in child.attrib['xsi:type']:
                    # Нашли шаг
                    return step
    return None

def pretty_print_element(elem):
    rough_string = ET.tostring(elem, encoding='utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ", encoding="utf-8").decode('utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Путь к xml-файлу')
    args = parser.parse_args()

    step = find_xsd_validation_step(args.input)
    if step is None:
        print('Шаг с валидацией по xsd-схеме не найден.')
        sys.exit(1)
    # Получаем имя шага
    step_name = step.attrib.get('Name', '(без имени)')
    print(f'Найден шаг с валидацией по xsd-схеме: Name="{step_name}". Это верный шаг? (y/n)')
    answer = input().strip().lower()
    if answer == 'y':
        print('\nВесь шаг целиком:\n')
        print(pretty_print_element(step))
    else:
        print('Операция отменена пользователем.')

if __name__ == '__main__':
    main() 