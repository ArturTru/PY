# Contact List App — автотесты

Тесты для https://qa-sendbox.org/  
Pytest + Playwright (sync), плюс несколько API-проверок.

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
playwright install chromium
```

## Запуск

```bash
source .venv/bin/activate

# всё
pytest tests/ -v

# smoke / acceptance
pytest tests/smoke -v -m smoke
pytest tests/acceptance -v -m acceptance

# только UI или API
pytest tests/smoke/test_ui.py tests/acceptance/test_ui.py -v
pytest tests/smoke/test_api.py tests/acceptance/test_api.py -v

# браузер видно
HEADLESS_MODE=False pytest tests/smoke/test_ui.py -v
```

Через скрипт: `./run_tests.sh all` (или `smoke`, `acceptance`, `ui`, `api`).

## Настройки

В `config/settings.py`:
- `APP_URL` — адрес приложения
- `HEADLESS_MODE` — `True` по умолчанию, `False` чтобы видеть браузер
- `SLOW_MO` — пауза между шагами в мс

Тестовый пользователь: `testuser@example.com` / `Test1234`

## Структура

```
config/settings.py
tests/
  smoke/test_ui.py, test_api.py
  acceptance/test_ui.py, test_api.py
  helpers/app_flows.py
  helpers/api_client.py
  conftest.py
```
