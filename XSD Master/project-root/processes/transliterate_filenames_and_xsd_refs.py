import os
import re
import argparse
import shutil

# Простая таблица транслитерации (ГОСТ/ISO)
TRANSLIT = {
    u'А': 'A', u'Б': 'B', u'В': 'V', u'Г': 'G', u'Д': 'D', u'Е': 'E', u'Ё': 'E', u'Ж': 'Zh', u'З': 'Z', u'И': 'I', u'Й': 'Y',
    u'К': 'K', u'Л': 'L', u'М': 'M', u'Н': 'N', u'О': 'O', u'П': 'P', u'Р': 'R', u'С': 'S', u'Т': 'T', u'У': 'U', u'Ф': 'F',
    u'Х': 'Kh', u'Ц': 'Ts', u'Ч': 'Ch', u'Ш': 'Sh', u'Щ': 'Shch', u'Ы': 'Y', u'Э': 'E', u'Ю': 'Yu', u'Я': 'Ya',
    u'Ь': '', u'Ъ': '',
    u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g', u'д': 'd', u'е': 'e', u'ё': 'e', u'ж': 'zh', u'з': 'z', u'и': 'i', u'й': 'y',
    u'к': 'k', u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o', u'п': 'p', u'р': 'r', u'с': 's', u'т': 't', u'у': 'u', u'ф': 'f',
    u'х': 'kh', u'ц': 'ts', u'ч': 'ch', u'ш': 'sh', u'щ': 'shch', u'ы': 'y', u'э': 'e', u'ю': 'yu', u'я': 'ya',
    u'ь': '', u'ъ': ''
}
def translit(s):
    return ''.join([TRANSLIT[c] if c in TRANSLIT else c for c in s])

def find_cyrillic(s):
    return re.search(r'[А-Яа-яЁё]', s)

def collect_files(root):
    files = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            files.append(os.path.join(dirpath, fn))
    return files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True, help='Папка для обработки')
    parser.add_argument('--main_xsd', required=False, help='Имя главной схемы (относительно корня)')
    parser.add_argument('--dry-run', action='store_true', help='Только показать, не переименовывать')
    args = parser.parse_args()
    files = collect_files(args.dir)
    rename_map = {}
    # ENG создаётся внутри args.dir
    eng_dir = os.path.join(os.path.abspath(args.dir.rstrip('/\\')), 'ENG')
    if not os.path.exists(eng_dir):
        os.makedirs(eng_dir)
    # Определяем основную схему
    main_xsd = None
    if args.main_xsd:
        for f in files:
            rel = os.path.relpath(f, args.dir)
            if rel.replace('\\','/').endswith(args.main_xsd.replace('\\','/')):
                main_xsd = f
                break
        if not main_xsd:
            print(f'Главная схема {args.main_xsd} не найдена!')
            return
    else:
        for f in files:
            rel = os.path.relpath(f, args.dir)
            if rel.count(os.sep) == 0 and f.lower().endswith('.xsd'):
                main_xsd = f
                break
        if not main_xsd:
            print('Не найдена основная XSD-схема в корне папки!')
            return
    # 1. Переименование файлов (только имена, не содержимое)
    for path in files:
        rel_path = os.path.relpath(path, args.dir)
        dirname, basename = os.path.split(rel_path)
        new_basename = translit(basename) if find_cyrillic(basename) else basename
        new_rel_path = os.path.join(dirname, new_basename)
        rename_map[rel_path] = new_rel_path
    # 2. Копирование файлов
    for path in files:
        rel_path = os.path.relpath(path, args.dir)
        new_rel_path = rename_map[rel_path]
        out_path = os.path.join(eng_dir, new_rel_path)
        out_dir = os.path.dirname(out_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        # Если это основная схема — меняем schemaLocation
        if os.path.abspath(path) == os.path.abspath(main_xsd):
            with open(path, encoding='utf-8') as f:
                text = f.read()
            orig_text = text
            # Меняем только schemaLocation (весь путь)
            def translit_schema_location(m):
                orig = m.group(3)
                new = translit(orig)
                if orig != new:
                    print(f'  schemaLocation: {orig} -> {new}')
                return f'{m.group(1)}{m.group(2)}{new}{m.group(4)}'
            text = re.sub(r'(schemaLocation\s*=\s*)(["\t])([^"\'\t]*)(["\'\t])', translit_schema_location, text)
            if text != orig_text:
                print(f'Обновляю schemaLocation в основной схеме: {new_rel_path}')
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            # Просто копируем файл с новым именем
            shutil.copy2(path, out_path)
            if rel_path != new_rel_path:
                print(f'Переименую файл: {rel_path} -> {new_rel_path}')
    print(f'Готово! Все файлы сохранены в: {eng_dir}')

if __name__ == '__main__':
    main() 