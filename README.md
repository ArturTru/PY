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

2. Создать и активировать виртуальное окружение
   python -m venv .venv
   source .venv/bin/activate      # Linux/macOS
   .venv\Scripts\activate        # Windows

3. Установить зависимости (проект установится в режиме editable)
   pip install -e .

   playwright install chromium
   playwright install-deps chromium   # только для Linux

4. Установить браузер Playwright
   playwright install chromium
   playwright install-deps chromium   # только для Linux

5. Запустить все тесты
   pytest tests/ -v

Запуск отдельных групп (по маркерам)
В проекте используются маркеры: smoke, acceptance, ui, api, crud, favorite, regression.

Команда	Запускаемые тесты
pytest -m smoke	Дымовые тесты
pytest -m ui	Все UI-тесты
pytest -m api	Все API-тесты
pytest -m crud	Тесты CRUD (создание/чтение/обновление/удаление)
pytest -m "smoke and ui"	Пересечение – дымовые UI-тесты
pytest -m "not api"	Все тесты, кроме API

Allure-отчёты
1. Запустить тесты с сохранением Allure-результатов
   pytest tests/ -v --alluredir=allure-results

2. Просмотреть отчёт локально (требуется установленный Allure CLI)
   allure serve allure-results

3. Сгенерировать статический HTML-отчёт
   allure generate allure-results -o allure-report --clean
   Открой allure-report/index.html в браузере.

Запуск через Docker
1. Собрать образ
   docker build -t contact-tests .

2. Запустить все тесты в контейнере
   docker run --rm -v $(pwd)/allure-results:/app/allure-results contact-tests

bash
docker run --rm -v $(pwd)/allure-results:/app/allure-results contact-tests

3. Запуск с помощью Docker Compose
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

