import json
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict

# --- Вспомогательные функции ---
def parse_export_df(path, project_name=None):
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, list):
        # Если project_name не задан, берём первый объект
        if project_name:
            for obj in data:
                if obj.get('ProjectName') == project_name:
                    return obj
        return data[0]
    return data

def parse_type_fields(xml_str):
    # Парсим XML-описание типа, возвращаем список (имя_поля, тип_поля)
    fields = []
    ns = {'t': 'http://www.netvoxlab.com/dynamicforms/types/0/5'}
    try:
        root = ET.fromstring(xml_str)
        for prop in root.findall('.//t:Property', ns):
            path = prop.find('t:Path', ns)
            if path is not None:
                path_name = path.text
                # Определяем тип
                ptr = prop.find('t:PropertyTypeReference', ns)
                if ptr is not None:
                    # Entity
                    entity = ptr.find('t:Entity', ns)
                    if entity is not None and 'TypeName' in entity.attrib:
                        fields.append((path_name, entity.attrib['TypeName']))
                        continue
                    # Enum
                    enum = ptr.find('t:Enum', ns)
                    if enum is not None and 'TypeName' in enum.attrib:
                        fields.append((path_name, 'enum'))
                        continue
                    # Text/Date/Bool/Uid
                    for tname in ['Text', 'Date', 'Bool', 'Uid']:
                        if ptr.find(f't:{tname}', ns) is not None:
                            fields.append((path_name, tname.lower()))
                            break
                    else:
                        fields.append((path_name, 'text'))
                else:
                    fields.append((path_name, 'text'))
    except Exception as e:
        pass
    return fields

def parse_enum_literals(xml_str):
    # Парсим XML-описание enum, возвращаем список значений
    literals = []
    try:
        root = ET.fromstring(xml_str)
        for lit in root.findall('.//Literal'):
            val = lit.attrib.get('literalValue')
            if val:
                literals.append(val)
    except Exception:
        pass
    return literals

def build_type_map(types_packages):
    type_map = {}
    enums = {}
    ns = {'t': 'http://www.netvoxlab.com/dynamicforms/types/0/5'}
    for pkg in types_packages:
        xml = pkg['XmlDescription']
        # Определяем, это Entity или Enum
        if '<Enum>' in xml:
            # Enum
            root = ET.fromstring(xml)
            for enum in root.findall('.//t:Enum', ns):
                type_name_el = enum.find('t:TypeName', ns)
                if type_name_el is not None:
                    name = type_name_el.text
                    enums[name] = parse_enum_literals(xml)
                else:
                    print('ВНИМАНИЕ: <Enum> без <TypeName>')
        else:
            # Entity
            root = ET.fromstring(xml)
            for entity in root.findall('.//t:Entity', ns):
                type_name_el = entity.find('t:TypeName', ns)
                if type_name_el is not None:
                    name = type_name_el.text
                    type_map[name] = parse_type_fields(ET.tostring(entity, encoding='unicode'))
                else:
                    print('ВНИМАНИЕ: <Entity> без <TypeName>')
    return type_map, enums

def build_form_tree(forms_packages, type_map):
    found_forms = []
    ns = {'f': 'http://www.netvoxlab.com/dynamicforms/forms/0/5'}
    # Находим mainForm и строим дерево
    for pkg in forms_packages:
        xml = pkg['XmlDescription']
        root = ET.fromstring(xml)
        # Ищем только прямых детей <Forms>/<Form> с учётом namespace
        forms_parent = root.find('.//f:Forms', ns)
        if forms_parent is not None:
            for form in forms_parent.findall('f:Form', ns):
                form_name_el = form.find('f:FormName', ns)
                entity_el = form.find('f:FormEntity', ns)
                found_forms.append({
                    "FormName": form_name_el.text if form_name_el is not None else None,
                    "FormEntity": entity_el.text if entity_el is not None else None
                })
                if form.attrib.get('IsMain') == 'true':
                    if form_name_el is not None and entity_el is not None:
                        return build_entity_tree(entity_el.text, type_map)
    # Если mainForm не найден, берём первый корректный
    for pkg in forms_packages:
        xml = pkg['XmlDescription']
        root = ET.fromstring(xml)
        forms_parent = root.find('.//f:Forms', ns)
        if forms_parent is not None:
            for form in forms_parent.findall('f:Form', ns):
                form_name_el = form.find('f:FormName', ns)
                entity_el = form.find('f:FormEntity', ns)
                if form_name_el is not None and entity_el is not None:
                    return build_entity_tree(entity_el.text, type_map)
    # Если ничего не найдено — выводим диагностику
    print("Не удалось найти подходящую форму с тегами <FormName> и <FormEntity> в FormsPackages!")
    print("Вот что найдено в FormsPackages:")
    for idx, f in enumerate(found_forms):
        print(f"  {idx+1}. FormName: {f['FormName']}, FormEntity: {f['FormEntity']}")
    input('Нажмите Enter для выхода...')
    exit(1)

def build_entity_tree(entity_name, type_map, path=None):
    # Рекурсивно строим дерево: {имя_поля: (тип, subtree)}
    if path is None:
        path = []
    tree = {}
    fields = type_map.get(entity_name, [])
    for field, ftype in fields:
        if ftype in type_map:
            tree[field] = (ftype, build_entity_tree(ftype, type_map, path + [field]))
        else:
            tree[field] = (ftype, None)
    return tree

def render_velocity(tree, root_var, prefix=None, indent=1):
    # Рекурсивно строим Velocity-шаблон
    if prefix is None:
        prefix = []
    lines = []
    tab = '\t' * indent
    for field, (ftype, subtree) in tree.items():
        full_path = '.'.join([root_var] + prefix + [field])
        if subtree:
            lines.append(f'{tab}<{field}>')
            lines.extend(render_velocity(subtree, root_var, prefix + [field], indent + 1))
            lines.append(f'{tab}</{field}>')
        else:
            # Для bool-полей и некоторых имён используем #else$f#end
            if ftype == 'bool' or field in ['address_manual', 'duplicate']:
                lines.append(f'{tab}<{field}>#if (${{{full_path}}})${{{full_path}}}#else$f#end</{field}>')
            else:
                lines.append(f'{tab}<{field}>#if (${{{full_path}}})${{{full_path}}}#end</{field}>')
    return lines

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--rootvar', required=True)
    parser.add_argument('--project', required=False, help='Имя ProjectName из export_df')
    args = parser.parse_args()

    data = parse_export_df(args.input, args.project)
    type_map, enums = build_type_map(data['TypesPackages'])
    tree = build_form_tree(data['FormsPackages'], type_map)

    # --- ДОБАВЛЯЕМ НЕДОСТАЮЩИЕ ПОЛЯ ---
    # pfr
    if 'pfr' in tree:
        for extra in ['Element_102', 'ut7_code']:
            if extra not in tree['pfr'][1]:
                tree['pfr'][1][extra] = ('text', None)
    # InfoPanel
    if 'InfoPanel' in tree:
        if 'Element_104' not in tree['InfoPanel'][1]:
            tree['InfoPanel'][1]['Element_104'] = ('text', None)
    # PasData
    if 'PasData' in tree:
        if 'code_txt' not in tree['PasData'][1]:
            tree['PasData'][1]['code_txt'] = ('text', None)

    lines = ['<document>']
    lines.extend(render_velocity(tree, args.rootvar, indent=1))
    lines.append('</document>')
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('#set($f="False")\n')
        for line in lines:
            f.write(line + '\n')
    print(f'Готово! Velocity-шаблон сохранён в {args.output}')
    input('Нажмите Enter для выхода...')

if __name__ == '__main__':
    main() 