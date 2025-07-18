# XSD Master

**XSD Master** — универсальный инструмент для автоматизации работы с XSD-схемами, генерации Velocity-шаблонов, валидации и транслитерации файлов и ссылок. Поддерживает современные UX-фичи, веб-интерфейс и автоматизацию всех этапов работы с XML/XSD.

---

## Проект автоматизации генерации и валидации XML для МЗАЗ

### Описание

Данный проект предназначен для автоматизации процесса генерации, проверки и анализа XML-файлов, соответствующих XSD-схемам, используемым в государственных интеграционных задачах (например, МЗАЗ). В проекте реализованы:
- Генерация шаблонов Velocity и примерных XML на их основе
- Извлечение переменных и данных из экспортируемых файлов
- Валидация XML по XSD-схемам с подробным анализом ошибок
- Вспомогательные утилиты для работы с формами и схемами
- Веб-интерфейс для запуска скриптов

### Структура папок

- `app.py` — Веб-интерфейс для запуска скриптов из браузера
- `generate_example_from_velocity.py` — Генерация примерного XML на основе Velocity-шаблона
- `generate_velocity_from_export_df.py` — Генерация Velocity-шаблона из export_df
- `extract_variables_from_export_df.py` — Извлечение переменных из export_df
- `extract_xml_from_export_task_both.py` — Извлечение XML из export_task для обеих форм
- `find_xsd_validation_step.py` — Поиск шага XSD-валидации в XML-процессе
- `xsd/` — Скрипты и файлы для валидации XML по XSD:
    - `validate_result.py` — Валидация XML по XSD с анализом ошибок
    - `velocity_xsd.xml` — Velocity-шаблон для генерации XML
    - `Результат.txt` — Сгенерированный XML для проверки
    - `example_result.xml` — Эталонный XML для сравнения
    - `validation_errors.txt` — Отчёт о найденных ошибках
- `valid/` — XSD-схемы (и их зависимости)
- `form1/`, `form2/` — Входные данные для разных форм (экспортированные файлы)

### Описание скриптов

### app.py
Веб-приложение (Flask), позволяющее запускать все скрипты из браузера, загружать входные файлы и просматривать вывод. Запуск:  
`python app.py`  
Откроется на http://127.0.0.1:5050

### generate_example_from_velocity.py
Генерирует пример XML-файла на основе Velocity-шаблона (`my_velocity.xml` или аналогичного). Заполняет все поля тестовыми значениями.  
**Пример запуска:**
```
python generate_example_from_velocity.py --input my_velocity.xml --output example_filled.xml
```

### generate_velocity_from_export_df.py
Генерирует Velocity-шаблон на основе файла `export_df` (JSON). Используется для автоматизации создания шаблонов под структуру форм.  
**Пример запуска:**
```
python generate_velocity_from_export_df.py --input form1/export_df --output my_velocity.xml --rootvar form0
```

### extract_variables_from_export_df.py
Извлекает все переменные, используемые в export_df, и сохраняет их в XML-список.  
**Пример запуска:**
```
python extract_variables_from_export_df.py
```

### extract_xml_from_export_task_both.py
Извлекает XML из файлов `export_task` для обеих форм и сохраняет их в `process_form1.xml` и `process_form2.xml`.  
**Пример запуска:**
```
python extract_xml_from_export_task_both.py
```

### find_xsd_validation_step.py
Находит шаг XSD-валидации в XML-процессе (например, в файле процесса интеграции).  
**Пример запуска:**
```
python find_xsd_validation_step.py --input process_form1.xml
```

### xsd/validate_result.py
Валидирует сгенерированный XML (`Результат.txt`) по XSD-схеме (`valid/MZAZ_2024-01-01.xsd`). Формирует подробный отчёт об ошибках с указанием расхождений с эталоном (`example_result.xml`).  
**Пример запуска:**
```
python xsd/validate_result.py
```

### Требования
- Python 3.7+
- Библиотеки: `xmlschema`, `flask` (для веб-интерфейса), стандартные библиотеки Python
- Для работы с Velocity-шаблонами требуется только Python (Java не нужен)

### Типовой сценарий работы
1. Сгенерировать Velocity-шаблон из export_df:
    ```
    python generate_velocity_from_export_df.py --input form1/export_df --output my_velocity.xml --rootvar form0
    ```
2. Сгенерировать пример XML:
    ```
    python generate_example_from_velocity.py --input my_velocity.xml --output example_filled.xml
    ```
3. Сгенерировать итоговый XML (например, через свой шаблонизатор или вручную)
4. Проверить XML на соответствие XSD и сравнить с эталоном:
    ```
    python xsd/validate_result.py
    ```
5. Изучить файл `xsd/validation_errors.txt` для анализа ошибок

### Авторы и поддержка
Вопросы и предложения — в Issues или напрямую разработчику.
