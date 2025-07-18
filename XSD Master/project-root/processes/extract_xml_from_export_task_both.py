import re
import os
import json
import sys
from xml.dom.minidom import parseString

XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8"?>\n'

def extract_and_save_xml(json_path, output_dir):
    if not os.path.exists(json_path):
        print(f'Файл {json_path} не найден!')
        return
    if not os.path.isdir(output_dir):
        print(f'Директория {output_dir} не найдена!')
        return
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = f.read()
        match = re.search(r'"RawValue"\s*:\s*"(.*?)"\s*,\s*\n', data, re.DOTALL)
        if not match:
            print(f'RawValue не найден в {json_path}!')
            return
        raw_value_escaped = match.group(1)
        xml = json.loads(f'"{raw_value_escaped}"')
        xml_str = xml.lstrip()
        if not xml_str.startswith('<?xml'):
            xml_str = XML_DECLARATION + xml_str
        dom = parseString(xml_str)
        pretty_xml = dom.toprettyxml(indent="    ", encoding="utf-8").decode("utf-8")
        pretty_xml = '\n'.join([line for line in pretty_xml.splitlines() if line.strip()])
        # Имя выходного файла: либо из переменной окружения, либо по умолчанию
        export_filename = os.environ.get('EXPORT_XML_FILENAME')
        if export_filename:
            out_name = export_filename
        else:
            out_name = os.path.splitext(os.path.basename(json_path))[0] + '.xml'
        output_path = os.path.join(output_dir, out_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        print(f'XML из {json_path} успешно извлечён и сохранён в {output_path}')
    except Exception as e:
        print(f'Ошибка при обработке {json_path}: {e}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Использование: python extract_xml_from_export_task_both.py <json_path> <output_dir>')
        sys.exit(1)
    json_path = sys.argv[1]
    output_dir = sys.argv[2]
    extract_and_save_xml(json_path, output_dir)