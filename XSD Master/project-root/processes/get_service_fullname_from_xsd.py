import re
import json
import sys
import uuid
from pathlib import Path
import argparse

# Пути к файлам теперь через аргументы командной строки
parser = argparse.ArgumentParser()
parser.add_argument('--xsd', required=True, help='Путь к XSD-схеме')
parser.add_argument('--json', required=True, help='Путь к JSON-файлу')
args = parser.parse_args()
xsd_path = args.xsd
json_path = args.json

# 1. Найти первое предложение, начинающееся с "Заявление"
def extract_service_fullname_from_xsd(xsd_file):
    with open(xsd_file, encoding='utf-8') as f:
        text = f.read()
    # Найти все <xs:documentation>...</xs:documentation>
    docs = re.findall(r'<xs:documentation>(.*?)</xs:documentation>', text, re.DOTALL)
    for doc in docs:
        # Найти первое предложение, начинающееся с "Заявление"
        match = re.search(r'(Заявление[^.]*\.)', doc)
        if match:
            return match.group(1).strip()
    return None

# 2. Заменить serviceFullName и id в prod_1507

def update_service_fullname_and_id_in_json(json_file, new_fullname):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    # Если это список с одним объектом
    if isinstance(data, list) and data:
        data[0]['serviceFullName'] = new_fullname
        data[0]['id'] = str(uuid.uuid4())
    else:
        raise Exception('Неожиданный формат prod_1507')
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    result = extract_service_fullname_from_xsd(xsd_path)
    if result:
        print(result)
    else:
        print('Не найдено подходящее описание в XSD.') 