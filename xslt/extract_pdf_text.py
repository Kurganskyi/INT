import pdfplumber
import os

# Путь к PDF-файлу в текущей папке
pdf_path = os.path.join(os.path.dirname(__file__), 'mzaz.pdf')
output_path = os.path.join(os.path.dirname(__file__), 'mzaz.txt')

text = ''
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + '\n'

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Текст из {pdf_path} сохранён в {output_path}') 