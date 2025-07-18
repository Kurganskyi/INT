import subprocess
import sys
import time
import webbrowser
import os

# Путь к app.py
SITE_DIR = os.path.join(os.path.dirname(__file__), 'site')
APP_PATH = os.path.join(SITE_DIR, 'app.py')

# Адрес сервера
HOST = '127.0.0.1'
PORT = 5050
URL = f'http://{HOST}:{PORT}/'

# Запуск Flask-сервера в отдельном процессе
proc = subprocess.Popen([sys.executable, APP_PATH], cwd=SITE_DIR)

# Ждём, пока сервер поднимется (можно улучшить через ping, но пока просто sleep)
time.sleep(2)

# Открываем в Chrome (если не найден, откроет в браузере по умолчанию)
try:
    chrome_path = None
    if sys.platform.startswith('win'):
        # Попытка найти Chrome на Windows
        import winreg
        reg_path = r'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe'
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                chrome_path = winreg.QueryValueEx(key, '')[0]
        except Exception:
            pass
        if not chrome_path:
            # Попробуем стандартный путь
            chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
            if not os.path.exists(chrome_path):
                chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
            if not os.path.exists(chrome_path):
                chrome_path = None
    elif sys.platform.startswith('darwin'):
        chrome_path = 'open -a "/Applications/Google Chrome.app" %s'
    else:
        chrome_path = '/usr/bin/google-chrome'
        if not os.path.exists(chrome_path):
            chrome_path = '/usr/bin/chromium-browser'
        if not os.path.exists(chrome_path):
            chrome_path = None
    if chrome_path and os.path.exists(chrome_path):
        webbrowser.get(f'"{chrome_path}" %s').open(URL)
    else:
        webbrowser.open(URL)
except Exception as e:
    print(f'Не удалось открыть Chrome автоматически: {e}')
    print(f'Откройте вручную: {URL}')

try:
    proc.wait()
except KeyboardInterrupt:
    print('Остановка сервера...')
    proc.terminate() 