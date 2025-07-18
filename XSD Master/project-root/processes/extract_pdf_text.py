import pdfplumber
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pdf', required=True, help='Путь к PDF-файлу')
parser.add_argument('--output', required=True, help='Путь к выходному текстовому файлу')
args = parser.parse_args()

pdf_path = args.pdf
output_path = args.output

text = ''
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Текст из {pdf_path} сохранён в {output_path}') 