import os
import subprocess
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

SCRIPTS = [f for f in os.listdir('.') if f.endswith('.py') and f != 'app.py']

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>VKUI Python Скрипты</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', 'Segoe UI', Arial, sans-serif;
            background: #f5f6fa;
            color: #222;
            margin: 0;
            padding: 0;
        }
        header {
            background: #fff;
            box-shadow: 0 2px 8px #0001;
            padding: 32px 0 16px 0;
            text-align: center;
        }
        header h1 {
            margin: 0;
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 1px;
        }
        .container {
            max-width: 800px;
            margin: 40px auto 0 auto;
            padding: 0 16px;
        }
        .script-block {
            margin-bottom: 32px;
            padding: 28px 24px 20px 24px;
            border-radius: 16px;
            background: #fff;
            box-shadow: 0 2px 16px #0002;
            border: none;
            transition: box-shadow 0.2s;
        }
        .script-block:hover {
            box-shadow: 0 6px 24px #0003;
        }
        .script-block h2 {
            margin-top: 0;
            font-size: 1.15rem;
            color: #5181B8;
            font-weight: 500;
        }
        label {
            color: #888;
            font-size: 1rem;
        }
        input[type="file"] {
            margin: 12px 0 18px 0;
            color: #222;
        }
        button {
            background: #5181B8;
            color: #fff;
            font-weight: 700;
            border: none;
            border-radius: 8px;
            padding: 12px 32px;
            font-size: 1.1rem;
            cursor: pointer;
            box-shadow: 0 2px 8px #0001;
            transition: background 0.2s, box-shadow 0.2s, transform 0.1s;
            display: inline-block;
        }
        button:hover {
            background: #4472a6;
            box-shadow: 0 4px 16px #0002;
            transform: translateY(-2px) scale(1.03);
        }
        .output {
            background: #f3f6fa;
            color: #222;
            padding: 16px;
            margin-top: 18px;
            border-radius: 10px;
            font-size: 1rem;
            border: 1px solid #e5e5e5;
            white-space: pre-wrap;
            max-height: 350px;
            overflow: auto;
        }
        footer {
            text-align: center;
            color: #b3b3b3;
            font-size: 1rem;
            margin: 40px 0 20px 0;
            opacity: 0.9;
        }
        @media (max-width: 600px) {
            .container { padding: 0 4px; }
            .script-block { padding: 14px 6px 10px 6px; }
        }
    </style>
</head>
<body>
    <header>
        <h1>VKUI Python-скрипты</h1>
        <div style="color:#5181B8; font-size:1.1rem; margin-top:8px;">Запускайте и тестируйте ваши утилиты прямо из браузера</div>
    </header>
    <div class="container">
    {% for script in scripts %}
    <form class="script-block" method="post" action="/run/{{script}}" enctype="multipart/form-data">
        <h2>{{script}}</h2>
        <label>Если скрипту нужны файлы — выберите их (можно пропустить):</label><br>
        <input type="file" name="input_file" multiple><br>
        <button type="submit">Запустить</button>
        {% if results and results[script] %}
        <div class="output">{{results[script]}}</div>
        {% endif %}
    </form>
    {% endfor %}
    </div>
    <footer>
        &copy; {{2024}} VKUI Python Utility Launcher
    </footer>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    results = {}
    return render_template_string(HTML_TEMPLATE, scripts=SCRIPTS, results=results)

@app.route('/run/<script>', methods=['POST'])
def run_script(script):
    if script not in SCRIPTS:
        return f"Скрипт {script} не найден!"
    files = request.files.getlist('input_file')
    filenames = []
    for file in files:
        if file.filename:
            fname = f"upload_{file.filename}"
            file.save(fname)
            filenames.append(fname)
    cmd = ['python', script] + filenames
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + '\n' + result.stderr
    except Exception as e:
        output = f"Ошибка запуска: {e}"
    for fname in filenames:
        if os.path.exists(fname):
            os.remove(fname)
    results = {script: output}
    return render_template_string(HTML_TEMPLATE, scripts=SCRIPTS, results=results)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5050) 