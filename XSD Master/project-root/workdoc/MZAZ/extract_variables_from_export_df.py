import json
import re
import os
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TASKS = [
    ('form1', 'variables_from_export_df_form1.xml'),
    ('form2', 'variables_from_export_df_form2.xml'),
]

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

for folder, out_name in TASKS:
    input_path = os.path.join(BASE_DIR, folder, 'export_df')
    output_path = os.path.join(BASE_DIR, out_name)
    variables = set()
    try:
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

input('Нажмите Enter для выхода...') 