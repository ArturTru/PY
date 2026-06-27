# Контакт-лист QA автотесты

Проект автоматизации тестирования демо-приложения [Contact List App](https://qa-sendbox.org/) с использованием **Python**, **Pytest**, **Playwright**, **Allure** и контейнеризацией через **Docker**. Легко запускается локально, в Docker или в **Jenkins** (в репозитории уже есть `Jenkinsfile`).

## 📌 Требования

| Инструмент | Версия (рекомендуемая) |
|------------|------------------------|
| Python     | 3.9 – 3.12             |
| pip        | последняя              |
| Docker     | 20.10+ (опционально)   |
| Docker Compose | 2.0+ (опционально) |
| Allure CLI | 2.13+ (для локального просмотра отчётов) |
| Jenkins    | 2.346+ (опционально)   |

## 🚀 Быстрый старт (локально)

1. **Клонировать репозиторий**  
   ```bash
   git clone https://github.com/ArturTru/PY.git
   cd PY


   python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate        # Windows

pip install -e .

playwright install chromium
playwright install-deps chromium   # только для Linux

pytest tests/ -v

апуск отдельных групп (по маркерам)
В проекте используются маркеры: smoke, acceptance, ui, api, crud, favorite, regression.

Команда	Запускаемые тесты
pytest -m smoke	Дымовые тесты
pytest -m ui	Все UI-тесты
pytest -m api	Все API-тесты
pytest -m crud	Тесты CRUD (создание/чтение/обновление/удаление)
pytest -m "smoke and ui"	Пересечение – дымовые UI-тесты
pytest -m "not api"	Все тесты, кроме API

Allure-отчёты
Запустить тесты с сохранением Allure-результатов
pytest tests/ -v --alluredir=allure-results

Просмотреть отчёт локально (требуется установленный Allure CLI)
allure serve allure-results

Сгенерировать статический HTML-отчёт
allure generate allure-results -o allure-report --clean
Открой allure-report/index.html в браузере.


Запуск через Docker
Собрать образ

bash
docker build -t contact-tests .
Запустить все тесты в контейнере

bash
docker run --rm -v $(pwd)/allure-results:/app/allure-results contact-tests
Запуск с помощью Docker Compose

bash
docker-compose up --build
(После завершения результаты Allure появятся в папке allure-results на хосте.)

⚙️ Запуск в Jenkins
В репозитории есть готовый Jenkinsfile для Declarative Pipeline.

Создайте новый Pipeline-проект в Jenkins.

В поле Pipeline script from SCM укажите:

URL репозитория: https://github.com/ArturTru/PY.git

Ветка: main

Путь к Jenkinsfile: Jenkinsfile

Запустите сборку.

Что делает Jenkinsfile:

Запускает этап Install & Test внутри Docker-контейнера с Python.

Устанавливает проект в режиме разработки, браузеры Playwright.

Запускает все тесты с генерацией Allure-результатов.

Всегда (даже при падении тестов) публикует Allure-отчёт (требуется плагин Allure Jenkins).

📂 Структура проекта
text
.
├── config/                # Настройки (URL, данные)
├── helpers/               # Вспомогательные функции (API, генераторы)
├── pages/                 # Page Objects
├── reports/               # Логи, скриншоты, JSON-слепки (создаётся автоматически)
├── tests/
│   ├── acceptance/        # Полные приёмочные сценарии (UI + API)
│   └── smoke/             # Дымовые тесты (базовая функциональность)
├── conftest.py            # Фикстуры, хуки для Allure-скриншотов
├── pyproject.toml         # Зависимости и конфигурация pytest
├── Dockerfile             # Образ для контейнеризации
├── docker-compose.yml     # (опционально) быстрый запуск
├── Jenkinsfile            # Pipeline для Jenkins
└── README.md              # Этот файл
📌 Дополнительные возможности
Параллельный запуск – установите pytest-xdist и запустите pytest -n auto tests/ – тесты распределятся по ядрам процессора.

Скриншоты при падении UI‑тестов автоматически прикрепляются к Allure-отчёту (реализовано в conftest.py).

API‑падения также сохраняют JSON‑ответы в Allure.

🆘 Возможные проблемы и решения
playwright не видит браузер – выполните playwright install chromium и проверьте наличие системных зависимостей (playwright install-deps chromium).

Ошибка прав при записи allure-results – в Jenkins добавлена команда chmod -R 777 allure-results (см. Jenkinsfile).

Неизвестный маркер – убедитесь, что в pyproject.toml в секции markers перечислены все используемые маркеры (они уже добавлены).

🤝 Вклад и поддержка
Проект открыт для улучшений. Если вы нашли ошибку или хотите предложить новую функциональность – создайте Issue или Pull Request.

