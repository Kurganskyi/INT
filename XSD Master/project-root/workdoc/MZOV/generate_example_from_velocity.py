import xml.etree.ElementTree as ET
import re
import argparse

# Словарь примеров для всех полей из my_velocity.xml
EXAMPLES = {
    # pfr
    'pfr': '12345',
    'reg_n': '987654',
    'date_z': '2024-01-01',
    'n': '555',
    'namePFR_txt': 'ПФР по Костромской области',
    'okato': '44000000000',
    'oktmo': '44701000001',
    'code': 'A1B2C3',
    'code1': 'D4E5F6',
    'Element_102': 'E102',
    'ut7_code': 'UT7CODE',
    # InfoPanel
    'stat': 'Мать',
    'F_Applicant': 'Иванова Мария Петровна',
    'f_pri_r': 'Петрова',
    'I_Applicant': 'Мария',
    'Ot_Applicant': 'Петровна',
    'date_birth': '1990-05-15',
    'snils': '123-456-789 00',
    'phone': '+7-900-000-00-00',
    'address_manual': 'true',
    'adr_reg_zayv': 'г. Кострома, ул. Ленина, д. 1',
    'address_type': 'Адрес регистрации',
    'adr_reg_zayv_fias': 'FIAS-REG-123',
    'adr_fact_zayv_fias': 'FIAS-FACT-456',
    'adr_preb_zayv_fias': 'FIAS-PREB-789',
    'Element_104': 'E104',
    # PasData
    'SelectTypeDoc': 'Паспорт гражданина РФ',
    'NameDoc': 'Паспорт',
    'Seria': '1234',
    'Number': '567890',
    'Seria_p': '4321',
    'Number_p': '098765',
    'DatePas': '2010-01-01',
    'srok_d': '2030-01-01',
    'kod_pdr': '770-001',
    'PassBy': 'ОВД г. Кострома',
    'code_txt': 'ПАСПОРТ',
    # certificate_info
    'seria': 'MK-123',
    'number': '1234567',
    'issued_date': '2022-12-31',
    'issued_by': 'ПФР',
    'duplicate': 'false',
    # predst
    'TypeDecl': '1',
    'StatusDecl': '2',
    'F_decl': 'Петров',
    'I_decl': 'Иван',
    'Ot_decl': 'Сергеевич',
    'Mesto_b': 'г. Кострома',
    'date_b': '1980-02-20',
    'grajdanstvo': '1',
    'grajdanstvo_txt': 'Российская Федерация',
    'adr_reg_pred': 'г. Кострома, ул. Советская, д. 2',
    'adr_reg_pred_fias': 'FIAS-REG-PRED-1',
    'adr_fact_pred_fias': 'FIAS-FACT-PRED-2',
    'adr_preb_pred_fias': 'FIAS-PREB-PRED-3',
    'phone_n': '+7-900-111-22-33',
    'pochta': 'predst@example.com',
    # predst.PasData
    'select_doc': 'Паспорт гражданина РФ',
    'date_v_pr': '2015-03-10',
    'kem_v': 'ОВД г. Кострома',
    # predst.Sved_poln
    'Polnom_pr': 'Доверенность',
    'datee_v': '2020-05-05',
    'sr_pol': '2025-05-05',
    'kem_vdn': 'Нотариус',
    # predst.recv
    'name': 'ООО Ромашка',
    'jur_address': 'г. Кострома, ул. Советская, д. 10',
    'fact_address': 'г. Кострома, ул. Советская, д. 11',
    'bank_finorg': 'Сбербанк',
    'inn': '4401000000',
    'ogrn': '1024400000000',
    'kpp': '440101001',
    'bik': '044525225',
    'ras_chet': '40702810900000000001',
    'cor_chet': '30101810400000000225',
    'email': 'info@romashka.ru',
    # uk_n_v
    'reason': '1',
    'date1': '2015-06-01',
    'date2': '2016-07-01',
    'date3': '2017-08-01',
    'reg_num': 'MZAZ-001',
    'operator': 'Иванова О.В.',
}

def strip_velocity(text):
    """Удаляет конструкции Velocity из строки."""
    text = re.sub(r'#if.*?#end', '', text, flags=re.DOTALL)
    text = re.sub(r'#else.*?#end', '', text, flags=re.DOTALL)
    text = re.sub(r'#set\(.*?\)', '', text)
    text = re.sub(r'#each', '', text)
    text = re.sub(r'#foreach.*?#end', '', text, flags=re.DOTALL)
    text = re.sub(r'#end', '', text)
    text = re.sub(r'#else', '', text)
    text = re.sub(r'#.*', '', text)
    text = re.sub(r'\$\{[^}]+\}', 'example', text)
    text = re.sub(r'\$[a-zA-Z_][a-zA-Z0-9_]*', 'example', text)
    return text

def parse_velocity_xml(velocity_path):
    with open(velocity_path, encoding='utf-8') as f:
        content = f.read()
    xml_content = strip_velocity(content)
    xml_content = '\n'.join(line for line in xml_content.splitlines() if '<' in line or '>' in line)
    try:
        root = ET.fromstring(xml_content)
    except Exception as e:
        print("Ошибка парсинга XML:", e)
        print("Проверьте, что шаблон содержит корректный XML после удаления Velocity.")
        exit(1)
    return root

def fill_example_data(elem):
    # Если есть вложенные теги — рекурсивно
    if list(elem):
        for child in elem:
            fill_example_data(child)
    else:
        # Используем словарь примеров
        name = elem.tag
        value = EXAMPLES.get(name, None)
        if value is not None:
            elem.text = value
        else:
            # Примерные значения по названию тега
            lname = name.lower()
            if 'date' in lname:
                elem.text = '2024-01-01'
            elif 'phone' in lname:
                elem.text = '+7-900-000-00-00'
            elif 'snils' in lname:
                elem.text = '123-456-789 00'
            elif 'email' in lname:
                elem.text = 'example@example.com'
            elif 'bool' in lname or 'flag' in lname or 'manual' in lname or 'duplicate' in lname:
                elem.text = 'true'
            elif 'code' in lname or 'id' in lname or 'num' in lname or 'number' in lname:
                elem.text = '12345'
            elif 'name' in lname or 'fio' in lname or 'surname' in lname or 'applicant' in lname:
                elem.text = 'Иванов Иван Иванович'
            else:
                elem.text = 'example'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Путь к Velocity-шаблону (например, my_velocity.xml)')
    parser.add_argument('--output', required=True, help='Путь для сохранения примера XML')
    args = parser.parse_args()

    root = parse_velocity_xml(args.input)
    fill_example_data(root)
    tree = ET.ElementTree(root)
    tree.write(args.output, encoding='utf-8', xml_declaration=True)
    print(f'Пример XML сохранён в {args.output}')

if __name__ == '__main__':
    main() 