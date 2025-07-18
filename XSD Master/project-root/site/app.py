import os
import glob
import subprocess
from flask import Flask, render_template_string, request, send_file
import tempfile
import shutil
import time
import uuid

app = Flask(__name__)

LAST_XML_PATH_FILE = '.last_xml_path'
LAST_VARS_XML_PATH_FILE = '.last_vars_xml_path'
LAST_VELOCITY_PATH_FILE = '.last_velocity_path'

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Извлечь xml из json</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Inter:400,500,700&display=swap" rel="stylesheet">
    <style>
        body {
            background: #18191c;
            font-family: 'YS Text', 'Inter', Arial, sans-serif;
            color: #f5f5f6;
            margin: 0;
            padding: 0;
        }
        header {
            background: #23242a;
            box-shadow: 0 2px 8px #0008;
            padding: 32px 0 16px 0;
            text-align: center;
            border-bottom: 1px solid #292a2e;
        }
        header h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 1px;
            color: #FFD600;
        }
        .main-flex {
            display: flex;
            flex-direction: row;
            gap: 32px;
            max-width: 1200px;
            margin: 40px auto 0 auto;
            padding: 0 16px;
            align-items: flex-start;
        }
        .left-col {
            flex: 1 1 350px;
            min-width: 320px;
            max-width: 500px;
        }
        .right-col {
            flex: 1 1 500px;
            min-width: 350px;
            max-width: 700px;
        }
        .lego-card {
            margin-bottom: 32px;
            padding: 32px 28px 24px 28px;
            border-radius: 16px;
            background: #23242a;
            box-shadow: 0 2px 8px #0006;
            border: 1px solid #292a2e;
            transition: box-shadow 0.2s, background 0.2s;
        }
        .lego-card:hover {
            box-shadow: 0 6px 24px #000a;
            background: #23242a;
        }
        .lego-card h2 {
            margin-top: 0;
            font-size: 1.15rem;
            color: #FFD600;
            font-weight: 600;
        }
        label {
            color: #bdbdbd;
            font-size: 1rem;
            font-weight: 500;
        }
        input[type="file"], input[type="text"], select {
            background: #18191c;
            color: #f5f5f6;
            border: 1.5px solid #393a3e;
            border-radius: 8px;
            padding: 12px 16px;
            margin: 8px 0 18px 0;
            font-size: 1.05rem;
            width: 100%;
            box-sizing: border-box;
            transition: border 0.2s;
        }
        input[type="file"]::-webkit-file-upload-button {
            background: #FFD600;
            color: #23242a;
            border: none;
            border-radius: 6px;
            padding: 8px 18px;
            font-size: 1rem;
            cursor: pointer;
            margin-right: 12px;
            font-weight: 500;
        }
        input[type="file"]::-webkit-file-upload-button:hover {
            background: #ffe066;
        }
        button, .lego-btn {
            background: #FFD600;
            color: #23242a;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 12px 32px;
            font-size: 1.1rem;
            cursor: pointer;
            box-shadow: 0 2px 8px #0003;
            transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
            display: inline-block;
        }
        button:hover, .lego-btn:hover {
            background: #ffe066;
            box-shadow: 0 4px 16px #0005;
            transform: translateY(-2px) scale(1.03);
        }
        .output {
            background: #23242a;
            color: #f5f5f6;
            padding: 16px;
            margin-top: 18px;
            border-radius: 10px;
            font-size: 1rem;
            border: 1.5px solid #393a3e;
            white-space: pre-wrap;
            max-height: 350px;
            overflow: auto;
        }
        .xml-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
            margin-top: 8px;
        }
        .xml-header-title {
            font-size: 1.08rem;
            color: #FFD600;
            font-weight: 600;
            letter-spacing: 0.5px;
        }
        .copy-btn {
            background: #FFD600;
            color: #23242a;
            border: none;
            border-radius: 6px;
            padding: 7px 18px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            margin-left: 16px;
            transition: background 0.2s;
        }
        .copy-btn:hover {
            background: #ffe066;
        }
        .xml-viewer {
            background: #18191c;
            color: #f5f5f6;
            padding: 18px;
            margin-top: 0;
            border-radius: 10px;
            font-size: 1rem;
            border: 1.5px solid #393a3e;
            white-space: pre;
            max-height: 700px;
            overflow: auto;
        }
        .notify {
            background: #23242a;
            color: #FFD600;
            border: 1.5px solid #FFD600;
            border-radius: 8px;
            padding: 12px 18px;
            margin-bottom: 18px;
            font-size: 1.1rem;
        }
        .notify.error {
            background: #2a1a1a;
            color: #ffbdbd;
            border: 1.5px solid #ffbdbd;
        }
        .next-step-btn {
            margin-top: 18px;
            width: 100%;
            background: linear-gradient(90deg, #FFD600 60%, #ffe066 100%);
            color: #23242a;
            font-size: 1.1rem;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 14px 0;
            box-shadow: 0 2px 8px #0003;
            transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
        }
        .next-step-btn:hover {
            background: linear-gradient(90deg, #ffe066 60%, #FFD600 100%);
            box-shadow: 0 4px 16px #0005;
            transform: translateY(-2px) scale(1.03);
        }
        footer {
            text-align: center;
            color: #bdbdbd;
            font-size: 1rem;
            margin: 40px 0 20px 0;
            opacity: 0.9;
        }
        @media (max-width: 900px) {
            .main-flex { flex-direction: column; gap: 0; }
            .right-col, .left-col { max-width: 100%; min-width: 0; }
        }
    </style>
    <script>
    function copyXmlCode() {
        const code = document.getElementById('xml-code-pre');
        if (code) {
            const text = code.innerText;
            navigator.clipboard.writeText(text).then(function() {
                const btn = document.getElementById('copy-btn');
                if (btn) {
                    btn.innerText = 'Скопировано!';
                    setTimeout(() => { btn.innerText = 'Копировать код'; }, 1200);
                }
            });
        }
    }
    function copyXmlVarsCode() {
        const code = document.getElementById('xml-vars-code-pre');
        if (code) {
            const text = code.innerText;
            navigator.clipboard.writeText(text).then(function() {
                const btn = document.getElementById('copy-btn-vars');
                if (btn) {
                    btn.innerText = 'Скопировано!';
                    setTimeout(() => { btn.innerText = 'Копировать код'; }, 1200);
                }
            });
        }
    }
    function copyVelocityCode() {
        const code = document.getElementById('velocity-code-pre');
        if (code) {
            const text = code.innerText;
            navigator.clipboard.writeText(text).then(function() {
                const btn = document.getElementById('copy-btn-velocity');
                if (btn) {
                    btn.innerText = 'Скопировано!';
                    setTimeout(() => { btn.innerText = 'Копировать код'; }, 1200);
                }
            });
        }
    }
    function updateMainXsdSelect(input) {
        var select = document.getElementById('main_xsd_select');
        select.innerHTML = '';
        var files = input.files;
        var xsdNames = [];
        for (var i = 0; i < files.length; i++) {
            var rel = files[i].webkitRelativePath || files[i].name;
            if (rel.match(/\.xsd$/i)) xsdNames.push(rel);
        }
        if (xsdNames.length === 0) {
            select.innerHTML = '<option value="">(нет .xsd файлов)</option>';
        } else {
            for (var i = 0; i < xsdNames.length; i++) {
                var opt = document.createElement('option');
                opt.value = xsdNames[i];
                opt.text = xsdNames[i];
                select.appendChild(opt);
            }
        }
        console.log('XSD-файлы для выбора:', xsdNames);
    }
    function updateMainXsdSelectVelocity(input) {
        var select = document.getElementById('main_xsd_select_velocity');
        select.innerHTML = '';
        var files = input.files;
        var xsdNames = [];
        for (var i = 0; i < files.length; i++) {
            var rel = files[i].webkitRelativePath || files[i].name;
            if (rel.match(/\.xsd$/i)) xsdNames.push(rel);
        }
        if (xsdNames.length === 0) {
            select.innerHTML = '<option value="">(нет .xsd файлов)</option>';
        } else {
            for (var i = 0; i < xsdNames.length; i++) {
                var opt = document.createElement('option');
                opt.value = xsdNames[i];
                opt.text = xsdNames[i];
                select.appendChild(opt);
            }
        }
        console.log('XSD-файлы для выбора (Velocity):', xsdNames);
    }
    function updateMainXsdSelectVelocityZip(input) {
        var select = document.getElementById('main_xsd_select_velocity');
        select.innerHTML = '';
        var file = input.files[0];
        if (!file || !file.name.match(/\.zip$/i)) {
            select.innerHTML = '<option value="">(нет .xsd файлов в архиве)</option>';
            return;
        }
        // Не можем прочитать содержимое архива на клиенте, просто показываем имя архива
        var opt = document.createElement('option');
        opt.value = file.name;
        opt.text = file.name + ' (архив будет обработан на сервере)';
        select.appendChild(opt);
    }
    function updateMainXsdSelectVelocityUnified(input) {
        var select = document.getElementById('main_xsd_select_velocity');
        select.innerHTML = '';
        var files = input.files;
        var xsdNames = [];
        var zipNames = [];
        for (var i = 0; i < files.length; i++) {
            var name = files[i].name;
            if (name.match(/\.xsd$/i)) xsdNames.push(name);
            else if (name.match(/\.zip$/i)) zipNames.push(name);
        }
        if (zipNames.length > 0) {
            // Если выбран архив, показываем его имя
            for (var i = 0; i < zipNames.length; i++) {
                var opt = document.createElement('option');
                opt.value = zipNames[i];
                opt.text = zipNames[i] + ' (архив будет обработан на сервере)';
                select.appendChild(opt);
            }
        } else if (xsdNames.length > 0) {
            for (var i = 0; i < xsdNames.length; i++) {
                var opt = document.createElement('option');
                opt.value = xsdNames[i];
                opt.text = xsdNames[i];
                select.appendChild(opt);
            }
        } else {
            select.innerHTML = '<option value="">(нет .xsd файлов или архивов)</option>';
        }
        console.log('Выбраны XSD:', xsdNames, 'ZIP:', zipNames);
    }
    </script>
</head>
<body>
    <header>
        <div style="display:flex;align-items:center;justify-content:center;gap:18px;">
            <span style="display:inline-block;height:64px;">
                <img src="{{ url_for('static', filename='logo.png') }}" alt="XSD Master Logo" style="height:64px; border-radius:16px;">
            </span>
            <h1 style="margin:0;">XSD Master</h1>
        </div>
        <div style="color:var(--text-accent); font-size:1.1rem; margin-top:8px;">Утилита для работы с XML, XSD и шаблонами</div>
    </header>
    <div class="main-flex">
      <div class="left-col">
        {% if notify %}
          <div class="notify {{notify_type}}">{{notify}}</div>
        {% endif %}
        <form class="lego-card" method="post" action="/extract_xml" enctype="multipart/form-data">
            <h2>Импорт JSON → XML</h2>
            <div style="color:#bdbdbd; font-size:0.98rem; margin-bottom:10px;">Преобразование JSON-файла в XML по шаблону. Быстрый импорт данных для дальнейшей работы.</div>
            <label>Выберите файл:</label><br>
            <input type="file" name="json_file"><br><br>
            <label>Имя выходного XML-файла (без .xml, опционально):</label><br>
            <input type="text" name="xml_filename" placeholder="example"><br><br>
            <label>Выберите директорию для сохранения:</label><br>
            <select name="output_dir">
                {% for d in dirs %}
                <option value="{{d}}">{{d}}</option>
                {% endfor %}
            </select><br><br>
            <button type="submit">Извлечь xml из json</button>
            {% if output %}
            <div class="output">{{output}}</div>
            {% endif %}
        </form>
        <form class="lego-card" method="post" action="/extract_vars" enctype="multipart/form-data" style="margin-top:0;">
            <h2>Извлечение переменных</h2>
            <div style="color:#bdbdbd; font-size:0.98rem; margin-bottom:10px;">Автоматическое извлечение переменных из export_df для шаблонов и проверки.</div>
            <label>Выберите export_df (JSON):</label><br>
            <input type="file" name="export_df_file"><br><br>
            <label>Имя выходного XML-файла (без .xml, опционально):</label><br>
            <input type="text" name="vars_xml_filename" placeholder="variables"><br><br>
            <label>Выберите директорию для сохранения:</label><br>
            <select name="output_dir">
                {% for d in dirs %}
                <option value="{{d}}">{{d}}</option>
                {% endfor %}
            </select><br><br>
            <button class="next-step-btn" type="submit">Извлечь переменные из export_df</button>
            {% if vars_output %}
            <div class="output">{{vars_output}}</div>
            {% endif %}
        </form>
        <form class="lego-card" method="post" action="/generate_velocity" enctype="multipart/form-data" style="margin-top:0;">
            <h2>Генерация Velocity-шаблона</h2>
            <div style="color:#bdbdbd; font-size:0.98rem; margin-bottom:10px;">Создание Velocity-шаблона на основе export_df для генерации XML.</div>
            <label>Выберите export_df (JSON):</label><br>
            <input type="file" name="export_df_file"><br><br>
            <label>rootvar (например, form0):</label><br>
            <input type="text" name="rootvar" placeholder="form0"><br><br>
            <label>ProjectName (опционально):</label><br>
            <input type="text" name="project_name" placeholder="(опционально)"><br><br>
            <label>Имя выходного файла (например, template.vm):</label><br>
            <input type="text" name="velocity_filename" placeholder="template.vm"><br><br>
            <label>Выберите директорию для сохранения:</label><br>
            <select name="output_dir">
                {% for d in dirs %}
                <option value="{{d}}">{{d}}</option>
                {% endfor %}
            </select><br><br>
            <button class="next-step-btn" type="submit">Сгенерировать Velocity-шаблон</button>
            {% if velocity_output %}
            <div class="output">{{velocity_output}}</div>
            {% endif %}
        </form>
        <form class="lego-card" method="post" action="/generate_velocity_xsd" enctype="multipart/form-data" style="margin-top:0;">
            <h2>Velocity по export_df + XSD</h2>
            <div style="color:#bdbdbd; font-size:0.98rem; margin-bottom:10px;">Генерация Velocity-шаблона с учётом структуры XSD и export_df.</div>
            <label>export_df (JSON):</label><br>
            <input type="file" name="export_df_file"><br><br>
            <label>XSD-файлы (выберите папку со схемами):</label><br>
            <input type="file" name="xsd_dir_file" webkitdirectory directory multiple onchange="updateMainXsdSelectVelocity(this)"><br><br>
            <label>Главная XSD-схема:</label><br>
            <select name="main_xsd" id="main_xsd_select_velocity"><option value="">(выберите после загрузки файлов)</option></select><br><br>
            <label>similar_xsd (опционально, XSD с похожими данными):</label><br>
            <input type="file" name="similar_xsd_file"><br><br>
            <label>rootvar (например, form0):</label><br>
            <input type="text" name="rootvar" placeholder="form0" value="form0"><br><br>
            <label>Имя выходного файла (например, template.vm):</label><br>
            <input type="text" name="velocity_filename" id="velocity_filename_xsd" placeholder="template.vm"><br><br>
            <label>Выберите директорию для сохранения:</label><br>
            <select name="output_dir">
                {% for d in dirs %}
                <option value="{{d}}">{{d}}</option>
                {% endfor %}
            </select><br><br>
            <button class="next-step-btn" type="submit">Сгенерировать Velocity по XSD</button>
            {% if velocity_xsd_output %}
            <div class="output">{{velocity_xsd_output}}</div>
            {% endif %}
        </form>
        <form class="lego-card" method="post" action="/transliterate_xsd" enctype="multipart/form-data" style="margin-top:0;">
            <h2>Транслитерация XSD</h2>
            <div style="color:#bdbdbd; font-size:0.98rem; margin-bottom:10px;">Преобразование имён файлов и ссылок XSD с кириллицы на латиницу для совместимости и стандартизации.</div>
            <label>Выберите папку с XSD-файлами:</label><br>
            <input type="file" name="xsd_dir_file" webkitdirectory directory multiple onchange="updateMainXsdSelect(this)"><br><br>
            <label>Главная XSD-схема:</label><br>
            <select name="main_xsd" id="main_xsd_select"><option value="">(выберите после загрузки файлов)</option></select><br><br>
            <button class="next-step-btn" type="submit">Преобразовать</button>
            {% if translit_output %}
            <div class="output">{{translit_output}}</div>
            {% endif %}
            {% if eng_zip_url %}
            <a href="{{ eng_zip_url }}" class="lego-btn" style="margin-top:12px;display:inline-block;">Скачать ENG (архив)</a>
            {% endif %}
        </form>
      </div>
      <div class="right-col">
        {% if xml_code %}
        <div class="xml-header">
            <span class="xml-header-title">Содержимое XML-файла:</span>
            <button class="copy-btn" id="copy-btn" type="button" onclick="copyXmlCode()">Копировать код</button>
        </div>
        <div class="xml-viewer">
            <pre id="xml-code-pre">{{xml_code}}</pre>
        </div>
        {% endif %}
        {% if vars_xml_code %}
        <div class="xml-header">
            <span class="xml-header-title">Содержимое XML с переменными:</span>
            <button class="copy-btn" id="copy-btn-vars" type="button" onclick="copyXmlVarsCode()">Копировать код</button>
        </div>
        <div class="xml-viewer">
            <pre id="xml-vars-code-pre">{{vars_xml_code}}</pre>
        </div>
        {% endif %}
        {% if velocity_code %}
        <div class="xml-header">
            <span class="xml-header-title">Velocity-шаблон:</span>
            <button class="copy-btn" id="copy-btn-velocity" type="button" onclick="copyVelocityCode()">Копировать код</button>
        </div>
        <div class="xml-viewer">
            <pre id="velocity-code-pre">{{velocity_code}}</pre>
        </div>
        {% endif %}
      </div>
    </div>
    <footer>
        &copy; 2025 AK Technology created<br>
        <span style="font-size:0.85em; color:#bdbdbd;">version {{ version }}</span>
    </footer>
</body>
</html>
'''

def get_version():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'version.txt'), encoding='utf-8') as f:
            return f.read().strip()
    except Exception:
        return '1.00'

@app.route('/', methods=['GET', 'POST'])
@app.route('/extract_xml', methods=['GET', 'POST'])
def extract_xml():
    notify = None
    notify_type = None
    output = None
    xml_code = None
    vars_output = None
    vars_xml_code = None
    velocity_output = None
    velocity_code = None
    # Получаем список директорий для сохранения
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    # Если GET — показать последние результаты для всех трёх окон
    if request.method == 'GET':
        # XML-файл
        if os.path.exists(LAST_XML_PATH_FILE):
            try:
                with open(LAST_XML_PATH_FILE, encoding='utf-8') as f:
                    last_xml_path = f.read().strip()
                if os.path.exists(last_xml_path):
                    with open(last_xml_path, encoding='utf-8') as f:
                        xml_code = f.read()
            except Exception:
                xml_code = None
        # XML с переменными
        if os.path.exists(LAST_VARS_XML_PATH_FILE):
            try:
                with open(LAST_VARS_XML_PATH_FILE, encoding='utf-8') as f:
                    last_vars_path = f.read().strip()
                if os.path.exists(last_vars_path):
                    with open(last_vars_path, encoding='utf-8') as f:
                        vars_xml_code = f.read()
            except Exception:
                vars_xml_code = None
        # Velocity
        if os.path.exists(LAST_VELOCITY_PATH_FILE):
            try:
                with open(LAST_VELOCITY_PATH_FILE, encoding='utf-8') as f:
                    last_velocity_path = f.read().strip()
                if os.path.exists(last_velocity_path):
                    with open(last_velocity_path, encoding='utf-8') as f:
                        velocity_code = f.read()
            except Exception:
                velocity_code = None
    last_xml_path = None
    if request.method == 'POST':
        file = request.files.get('json_file')
        output_dir = request.form.get('output_dir')
        xml_filename = request.form.get('xml_filename', '').strip()
        if not file or not output_dir:
            notify = 'Пожалуйста, выберите JSON-файл и директорию.'
            notify_type = 'error'
        else:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
                file.save(tmp.name)
                temp_json_path = tmp.name
            if xml_filename:
                base_name = xml_filename + '.xml'
            elif file.filename:
                base_name = os.path.splitext(os.path.basename(file.filename))[0] + '.xml'
            else:
                base_name = os.path.splitext(os.path.basename(temp_json_path))[0] + '.xml'
            last_xml_path = os.path.join(output_dir, base_name)
            env = os.environ.copy()
            env['EXPORT_XML_FILENAME'] = base_name
            cmd = ['python', os.path.join('..', 'processes', 'extract_xml_from_export_task_both.py'), temp_json_path, output_dir]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60, env=env)
                output = result.stdout + '\n' + result.stderr
                if 'успешно извлечён' in output and os.path.exists(last_xml_path):
                    notify = 'XML успешно извлечён!'
                    notify_type = ''
                    with open(last_xml_path, encoding='utf-8') as f:
                        xml_code = f.read()
                    # Сохраняем путь к последнему XML-файлу
                    with open(LAST_XML_PATH_FILE, 'w', encoding='utf-8') as f:
                        f.write(last_xml_path)
                else:
                    notify = 'Ошибка при извлечении XML.'
                    notify_type = 'error'
            except Exception as e:
                output = f'Ошибка запуска: {e}'
                notify = 'Ошибка запуска скрипта.'
                notify_type = 'error'
            finally:
                try:
                    os.remove(temp_json_path)
                except Exception:
                    pass
    return render_template_string(HTML_TEMPLATE, notify=notify, notify_type=notify_type, dirs=dirs, output=output, xml_code=xml_code, vars_output=vars_output, vars_xml_code=vars_xml_code, velocity_output=velocity_output, velocity_code=velocity_code, version=get_version())

@app.route('/extract_vars', methods=['POST'])
def extract_vars():
    notify = None
    notify_type = None
    vars_output = None
    vars_xml_code = None
    velocity_output = None
    velocity_code = None
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    file = request.files.get('export_df_file')
    output_dir = request.form.get('output_dir')
    vars_xml_filename = request.form.get('vars_xml_filename', '').strip()
    if not file or not output_dir:
        notify = 'Пожалуйста, выберите export_df и директорию.'
        notify_type = 'error'
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            file.save(tmp.name)
            temp_json_path = tmp.name
        if vars_xml_filename:
            base_name = vars_xml_filename + '.xml'
        elif file.filename:
            base_name = os.path.splitext(os.path.basename(file.filename))[0] + '.xml'
        else:
            base_name = os.path.splitext(os.path.basename(temp_json_path))[0] + '.xml'
        last_xml_path = os.path.join(output_dir, base_name)
        cmd = ['python', os.path.join('..', 'processes', 'extract_variables_from_export_df.py'), temp_json_path, output_dir, base_name]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            vars_output = result.stdout + '\n' + result.stderr
            if os.path.exists(last_xml_path):
                with open(last_xml_path, encoding='utf-8') as f:
                    vars_xml_code = f.read()
                # Сохраняем путь к последнему XML с переменными
                with open(LAST_VARS_XML_PATH_FILE, 'w', encoding='utf-8') as f:
                    f.write(last_xml_path)
        except Exception as e:
            vars_output = f'Ошибка запуска: {e}'
        finally:
            try:
                os.remove(temp_json_path)
            except Exception:
                pass
    return render_template_string(HTML_TEMPLATE, notify=None, notify_type=None, dirs=dirs, output=None, xml_code=None, vars_output=vars_output, vars_xml_code=vars_xml_code, velocity_output=velocity_output, velocity_code=velocity_code, version=get_version())

@app.route('/generate_velocity', methods=['POST'])
def generate_velocity():
    notify = None
    notify_type = None
    velocity_output = None
    velocity_code = None
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    file = request.files.get('export_df_file')
    output_dir = request.form.get('output_dir')
    velocity_filename = request.form.get('velocity_filename', '').strip()
    rootvar = request.form.get('rootvar', '').strip()
    project_name = request.form.get('project_name', '').strip()
    if not file or not output_dir or not velocity_filename or not rootvar:
        notify = 'Пожалуйста, выберите export_df, директорию, укажите rootvar и имя выходного файла.'
        notify_type = 'error'
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            file.save(tmp.name)
            temp_json_path = tmp.name
        last_velocity_path = os.path.join(output_dir, velocity_filename)
        cmd = ['python', os.path.join('..', 'processes', 'generate_velocity_from_export_df.py'),
               '--input', temp_json_path,
               '--output', last_velocity_path,
               '--rootvar', rootvar]
        if project_name:
            cmd.extend(['--project', project_name])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
            velocity_output = result.stdout + '\n' + result.stderr
            if os.path.exists(last_velocity_path):
                with open(last_velocity_path, encoding='utf-8') as f:
                    velocity_code = f.read()
                # Сохраняем путь к последнему Velocity
                with open(LAST_VELOCITY_PATH_FILE, 'w', encoding='utf-8') as f:
                    f.write(last_velocity_path)
        except Exception as e:
            velocity_output = f'Ошибка запуска: {e}'
        finally:
            try:
                os.remove(temp_json_path)
            except Exception:
                pass
    return render_template_string(HTML_TEMPLATE, notify=None, notify_type=None, dirs=dirs, output=None, xml_code=None, vars_output=None, vars_xml_code=None, velocity_output=velocity_output, velocity_code=velocity_code, version=get_version())

@app.route('/generate_velocity_xsd', methods=['POST'])
def generate_velocity_xsd():
    import tempfile, shutil, subprocess, zipfile
    notify = None
    notify_type = None
    velocity_xsd_output = None
    velocity_code = None
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    export_df_file = request.files.get('export_df_file')
    xsd_dir_files = request.files.getlist('xsd_files')
    main_xsd_name = request.form.get('main_xsd', '').strip()
    similar_xsd_file = request.files.get('similar_xsd_file')
    output_dir = request.form.get('output_dir')
    velocity_filename = request.form.get('velocity_filename', '').strip()
    rootvar = request.form.get('rootvar', '').strip()

    # --- Новый этап: если main_xsd не выбран, показать список XSD после распаковки ---
    with tempfile.TemporaryDirectory() as temp_dir:
        export_df_path = os.path.join(temp_dir, 'export_df.json')
        if export_df_file:
            export_df_file.save(export_df_path)
        xsd_dir_path = os.path.join(temp_dir, 'xsd_dir')
        os.makedirs(xsd_dir_path, exist_ok=True)
        xsd_files_saved = []
        # Сохраняем все загруженные файлы (XSD и ZIP)
        for f in xsd_dir_files:
            if f and getattr(f, 'filename', None) and f.filename:
                rel_path = f.filename.replace('\\', '/').replace('..', '')
                save_path = os.path.join(xsd_dir_path, rel_path)
                save_dir = os.path.dirname(save_path)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir, exist_ok=True)
                f.save(save_path)
                xsd_files_saved.append(save_path)
        # Распаковываем все ZIP-архивы
        for file_path in xsd_files_saved:
            if file_path.lower().endswith('.zip'):
                try:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(xsd_dir_path)
                except Exception as e:
                    notify = f'Ошибка при распаковке архива {os.path.basename(file_path)}: {e}'
                    notify_type = 'error'
                    return render_template_string(HTML_TEMPLATE, notify=notify, notify_type=notify_type, dirs=dirs, output=None, xml_code=None, vars_output=None, vars_xml_code=None, velocity_output=None, velocity_code=None, velocity_xsd_output=None, version=get_version())
        # Собираем список всех XSD-файлов после распаковки
        all_xsd_files = []
        for root, _, files in os.walk(xsd_dir_path):
            for fname in files:
                if fname.lower().endswith('.xsd'):
                    rel_path = os.path.relpath(os.path.join(root, fname), xsd_dir_path)
                    all_xsd_files.append(rel_path)
        # Если main_xsd не выбран, показать форму выбора главной схемы
        if not main_xsd_name:
            notify = 'Выберите главную XSD-схему из загруженных файлов.'
            return render_template_string(HTML_TEMPLATE, notify=notify, notify_type='info', dirs=dirs, output=None, xml_code=None, vars_output=None, vars_xml_code=None, velocity_output=None, velocity_code=None, velocity_xsd_output=None, main_xsd_options=all_xsd_files, version=get_version())
        # --- Если main_xsd выбран, продолжаем как обычно ---
        assert main_xsd_name
        similar_xsd_path = None
        if similar_xsd_file and getattr(similar_xsd_file, 'filename', None) and similar_xsd_file.filename:
            similar_xsd_path = os.path.join(temp_dir, 'similar.xsd')
            similar_xsd_file.save(similar_xsd_path)
        last_velocity_path = os.path.join(output_dir, velocity_filename)
        main_xsd_path = os.path.join(xsd_dir_path, main_xsd_name)
        cmd = [
            'python', os.path.join('..', 'processes', 'generate_velocity_from_export_df_and_xsd.py'),
            '--export_df', export_df_path,
            '--main_xsd', main_xsd_path,
            '--xsd_dir', xsd_dir_path,
            '--rootvar', rootvar,
            '--output', last_velocity_path
        ]
        if similar_xsd_path:
            cmd.extend(['--similar_xsd', similar_xsd_path])
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            velocity_xsd_output = result.stdout + '\n' + result.stderr
            if os.path.exists(last_velocity_path):
                with open(last_velocity_path, encoding='utf-8') as f:
                    velocity_code = f.read()
                with open(LAST_VELOCITY_PATH_FILE, 'w', encoding='utf-8') as f:
                    f.write(last_velocity_path)
        except Exception as e:
            velocity_xsd_output = f'Ошибка запуска: {e}'
    return render_template_string(HTML_TEMPLATE, notify=notify, notify_type=notify_type, dirs=dirs, output=None, xml_code=None, vars_output=None, vars_xml_code=None, velocity_output=None, velocity_code=velocity_code, velocity_xsd_output=velocity_xsd_output, version=get_version())

@app.route('/transliterate_xsd', methods=['POST'])
def transliterate_xsd():
    translit_output = None
    eng_zip_url = None
    dirs = [d for d in os.listdir('.') if os.path.isdir(d)]
    xsd_dir_files = request.files.getlist('xsd_dir_file')
    main_xsd_name = request.form.get('main_xsd', '').strip()
    if not xsd_dir_files:
        translit_output = 'Пожалуйста, выберите папку с XSD-файлами.'
    elif not main_xsd_name:
        translit_output = 'Пожалуйста, выберите главную XSD-схему.'
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            xsd_dir_path = os.path.join(temp_dir, 'xsd_dir')
            os.makedirs(xsd_dir_path, exist_ok=True)
            for f in xsd_dir_files:
                if f and getattr(f, 'filename', None) and f.filename:
                    save_path = os.path.join(xsd_dir_path, f.filename)
                    save_dir = os.path.dirname(save_path)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir, exist_ok=True)
                    f.save(save_path)
            translit_cmd = [
                'python', os.path.join('..', 'processes', 'transliterate_filenames_and_xsd_refs.py'),
                '--dir', xsd_dir_path,
                '--main_xsd', main_xsd_name
            ]
            try:
                translit_result = subprocess.run(translit_cmd, capture_output=True, text=True, timeout=60)
                translit_output = translit_result.stdout + '\n' + translit_result.stderr
                # Архивируем ENG в static/eng_zips
                eng_dir = os.path.join(xsd_dir_path, 'ENG')
                if os.path.exists(eng_dir):
                    static_zip_dir = os.path.join('static', 'eng_zips')
                    if not os.path.exists(static_zip_dir):
                        os.makedirs(static_zip_dir)
                    # Очистка старых архивов (старше 1 дня)
                    now = time.time()
                    for fname in os.listdir(static_zip_dir):
                        fpath = os.path.join(static_zip_dir, fname)
                        if os.path.isfile(fpath) and fname.endswith('.zip'):
                            if now - os.path.getmtime(fpath) > 86400:
                                try:
                                    os.remove(fpath)
                                except Exception:
                                    pass
                    zip_name = f'ENG_{int(time.time())}_{uuid.uuid4().hex[:8]}.zip'
                    eng_zip = os.path.join(static_zip_dir, zip_name)
                    shutil.make_archive(eng_zip[:-4], 'zip', eng_dir)
                    eng_zip_url = '/'+eng_zip.replace('\\','/')
            except Exception as e:
                translit_output = f'Ошибка транслитерации: {e}'
    return render_template_string(HTML_TEMPLATE, notify=None, notify_type=None, dirs=dirs, output=None, xml_code=None, vars_output=None, vars_xml_code=None, velocity_output=None, velocity_code=None, velocity_xsd_output=None, translit_output=translit_output, eng_zip_url=eng_zip_url, version=get_version())

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050) 