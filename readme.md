[![Python application](https://github.com/vasgg/coindesk_parser/actions/workflows/python-app.yml/badge.svg)](https://github.com/vasgg/coindesk_parser/actions/workflows/python-app.yml)

**Парсер новостей о биткоине с сайта CoinDesk.com**

Начало работы:

1. Установите последнюю версию Python.
2. Создайте виртуальное окружение.
3. Установите зависимости:

`pip install -r requirements.txt`

4. Запустите файл parser.py

`python3 parser.py`

Скрипт можно запускать с параметрами:

--days (по умолчанию - 60. Запрос новостей за последние 60 дней.)

--delay (по умолчанию - 0. Установка задержки между запросами в секундах.)

`python3 parser.py --days 1000 --delay 3`

Скрипт создаёт .csv файл и сохраняет его в папке 'exports'
