import os
import sys
import json
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
from argparse import ArgumentParser

# --- Вспомогательные функции ---
def autoclean_json_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    cleaned = re.sub(r',\s*([}\]])', r'\1', text)
    if cleaned != text:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return True
    return False

def parse_export_df_vars(export_df_path):
    with open(export_df_path, encoding='utf-8') as f:
        data = json.load(f)
    variables = set()
    def extract_from_xml(xml_str):
        # Ищем <Property>...</Property> и <Path>...</Path>
        props = re.findall(r'<Property>(.*?)</Property>', xml_str)
        paths = re.findall(r'<Path>(.*?)</Path>', xml_str)
        variables.update(props)
        variables.update(paths)
        for m in re.findall(r'hostObject\.GetValue\("~(.*?)"\)', xml_str):
            variables.add(m)
        for m in re.findall(r'\$\{([a-zA-Z0-9_\.]+)\}', xml_str):
            variables.add(m)
    for item in data:
        for fp in item.get('FormsPackages', []):
            extract_from_xml(fp.get('XmlDescription', ''))
        for tp in item.get('TypesPackages', []):
            extract_from_xml(tp.get('XmlDescription', ''))
    return set(v for v in variables if v and v != '')

def parse_similar_xsd_vars(similar_xsd_path):
    # Извлекает имена всех листовых элементов из similar_xsd
    tree = ET.parse(similar_xsd_path)
    root = tree.getroot()
    nsmap = {'xs': 'http://www.w3.org/2001/XMLSchema'}
    vars = set()
    def walk(element, prefix=None):
        if prefix is None:
            prefix = []
        name = element.attrib.get('name')
        ct = element.find('xs:complexType', nsmap)
        if ct is not None:
            seq = ct.find('xs:sequence', nsmap)
            if seq is not None:
                for child in seq.findall('xs:element', nsmap):
                    walk(child, prefix + [name] if name else prefix)
                return
        # leaf
        if name:
            vars.add('.'.join(prefix + [name]))
    for el in root.findall('xs:element', nsmap):
        walk(el)
    return vars

def parse_xsd_tree(main_xsd_path, xsd_dir):
    # Рекурсивно парсим XSD и все импорты, возвращаем дерево элементов
    parsed = {}
    def parse_file(xsd_path):
        if xsd_path in parsed:
            return parsed[xsd_path]
        tree = ET.parse(xsd_path)
        root = tree.getroot()
        nsmap = {'xs': 'http://www.w3.org/2001/XMLSchema'}
        elements = []
        # Импортируемые схемы
        for imp in root.findall('xs:import', nsmap):
            schema_loc = imp.attrib.get('schemaLocation')
            if schema_loc:
                import_path = os.path.join(xsd_dir, os.path.basename(schema_loc))
                parse_file(import_path)
        # Собираем элементы верхнего уровня
        for el in root.findall('xs:element', nsmap):
            elements.append(el)
        parsed[xsd_path] = elements
        return elements
    parse_file(main_xsd_path)
    # Собираем дерево начиная с корневого элемента
    def build_tree(element, nsmap):
        name = element.attrib.get('name')
        children = []
        ct = element.find('xs:complexType', nsmap)
        if ct is not None:
            seq = ct.find('xs:sequence', nsmap)
            if seq is not None:
                for child in seq.findall('xs:element', nsmap):
                    children.append(build_tree(child, nsmap))
        return {'name': name, 'children': children}
    # Берём первый корневой элемент
    all_elements = parsed[main_xsd_path]
    if not all_elements:
        raise Exception('В основной XSD не найдено ни одного xs:element')
    root_el = all_elements[0]
    return build_tree(root_el, {'xs': 'http://www.w3.org/2001/XMLSchema'})

def render_velocity_from_xsd(tree, export_vars, rootvar, prefix=None, indent=1, not_found=None, similar_vars=None, zapolnit_counter=None):
    if prefix is None:
        prefix = []
    if not_found is None:
        not_found = []
    if similar_vars is None:
        similar_vars = set()
    if zapolnit_counter is None:
        zapolnit_counter = {'n': 1}
    lines = []
    tab = '\t' * indent
    for child in tree.get('children', []):
        field = child['name']
        full_path = '.'.join([rootvar] + prefix + [field])
        # Сопоставление: ищем переменную с таким именем
        var_match = None
        for v in export_vars:
            if v.split('.')[-1] == field:
                var_match = v
                break
        similar_match = None
        if not var_match:
            for s in similar_vars:
                if s.split('.')[-1] == field:
                    similar_match = s
                    break
        if child.get('children'):
            lines.append(f'{tab}<{field}>')
            lines.extend(render_velocity_from_xsd(child, export_vars, rootvar, prefix + [field], indent + 1, not_found, similar_vars, zapolnit_counter))
            lines.append(f'{tab}</{field}>')
        else:
            if var_match:
                lines.append(f'{tab}<{field}>#if (${{{var_match}}})${{{var_match}}}#end</{field}>')
            elif similar_match:
                lines.append(f'{tab}<{field}>#if (${{{similar_match}}})${{{similar_match}}}#end</{field}>')
            else:
                zapolnit_name = f'ZAPOLNIT_PEREMENNUY_{zapolnit_counter["n"]}'
                lines.append(f'{tab}<{field}>${{{zapolnit_name}}}</{field}>')
                zapolnit_counter["n"] += 1
                not_found.append('.'.join(prefix + [field]))
    return lines

def main():
    parser = ArgumentParser()
    parser.add_argument('--export_df', required=True)
    parser.add_argument('--main_xsd', required=True)
    parser.add_argument('--xsd_dir', required=True)
    parser.add_argument('--rootvar', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--similar_xsd', required=False, help='Путь к XSD с похожими данными (опционально)')
    args = parser.parse_args()

    cleaned = autoclean_json_file(args.export_df)
    if cleaned:
        print('Внимание: исходный JSON был автоматически исправлен (удалены лишние запятые).')

    export_vars = parse_export_df_vars(args.export_df)
    xsd_tree = parse_xsd_tree(args.main_xsd, args.xsd_dir)
    similar_vars = set()
    if args.similar_xsd:
        similar_vars = parse_similar_xsd_vars(args.similar_xsd)
    not_found = []
    zapolnit_counter = {'n': 1}
    lines = ['<document>']
    lines.extend(render_velocity_from_xsd(xsd_tree, export_vars, args.rootvar, indent=1, not_found=not_found, similar_vars=similar_vars, zapolnit_counter=zapolnit_counter))
    lines.append('</document>')
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('#set($f="False")\n')
        for line in lines:
            f.write(line + '\n')
    print(f'Готово! Velocity-шаблон сохранён в {args.output}')
    if not_found:
        print('ВНИМАНИЕ: следующие поля из XSD не найдены в export_df и similar_xsd:')
        for nf in not_found:
            print('  -', nf)

if __name__ == '__main__':
    main() 