import json
import re
import os
import sys
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def autoclean_json_file(path):
    """Удаляет лишние запятые перед ] и } в JSON-файле."""
    with open(path, encoding='utf-8') as f:
        text = f.read()
    # Удаляем запятые перед ] и }
    cleaned = re.sub(r',\s*([}\]])', r'\1', text)
    if cleaned != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return True
    return False

def extract_from_xml(xml_str, variables):
    # Ищем <Property>...</Property> и <Path>...</Path>
    props = re.findall(r'<Property>(.*?)</Property>', xml_str)
    paths = re.findall(r'<Path>(.*?)</Path>', xml_str)
    variables.update(props)
    variables.update(paths)
    # Ищем переменные в скриптах вида hostObject.GetValue("~var")
    for m in re.findall(r'hostObject\.GetValue\("~(.*?)"\)', xml_str):
        variables.add(m)
    # Ищем переменные вида ${form0.pfr.ut7_code}
    for m in re.findall(r'\$\{([a-zA-Z0-9_\.]+)\}', xml_str):
        variables.add(m)

def main():
    if len(sys.argv) < 4:
        print('Usage: python extract_variables_from_export_df.py <input_json> <output_dir> <output_filename.xml>')
        sys.exit(1)
    input_path = sys.argv[1]
    output_dir = sys.argv[2]
    output_filename = sys.argv[3]
    output_path = os.path.join(output_dir, output_filename)
    variables = set()
    try:
        cleaned = autoclean_json_file(input_path)
        if cleaned:
            print('Внимание: исходный JSON был автоматически исправлен (удалены лишние запятые).')
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            for fp in item.get('FormsPackages', []):
                extract_from_xml(fp.get('XmlDescription', ''), variables)
            for tp in item.get('TypesPackages', []):
                extract_from_xml(tp.get('XmlDescription', ''), variables)
        variables = sorted(set(v for v in variables if v and v != ''))
        root = ET.Element('Variables')
        for var in variables:
            ET.SubElement(root, 'Variable').text = var
        # Преобразуем в строку и делаем pretty-print
        rough_string = ET.tostring(root, encoding='utf-8')
        dom = parseString(rough_string)
        pretty_xml = dom.toprettyxml(indent="    ", encoding="utf-8").decode("utf-8")
        # Удаляем пустые строки
        pretty_xml = '\n'.join([line for line in pretty_xml.splitlines() if line.strip()])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        print(f'Найдено {len(variables)} переменных в {input_path}. XML сохранён в {output_path}')
    except Exception as e:
        print(f'Ошибка при обработке {input_path}: {e}')

if __name__ == '__main__':
    main() 