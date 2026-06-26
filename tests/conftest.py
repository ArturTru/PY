# pylint: disable=redefined-outer-name

import logging
import json
import pytest
from datetime import datetime
from pathlib import Path

import allure  # <-- ALLURE: added for attaching reports

from playwright.sync_api import sync_playwright

from config.settings import APP_URL, BROWSER_TYPE, HEADLESS_MODE, SLOW_MO, TEST_DATA
from helpers.api_client import get_auth_token

# Page Object
from pages.login_page import LoginPage
from pages.contacts_page import ContactsPage

REPORTS_DIR = Path(__file__).parent.parent / "reports"


@pytest.fixture(scope="session")
def app_url():
    return APP_URL


@pytest.fixture
def browser():
    with sync_playwright() as pw:
        browsers = {
            "firefox": pw.firefox,
            "webkit": pw.webkit,
            "chromium": pw.chromium,
        }
        launcher = browsers.get(BROWSER_TYPE, pw.chromium)
        if SLOW_MO:
            br = launcher.launch(headless=HEADLESS_MODE, slow_mo=SLOW_MO)
        else:
            br = launcher.launch(headless=HEADLESS_MODE)
        yield br
        br.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1280, "height": 720})
    pg = context.new_page()
    yield pg
    context.close()


# PAGE OBJECT FIXTURES

@pytest.fixture
def login_page(page, app_url):
    """Login page object"""
    return LoginPage(page, app_url)


@pytest.fixture
def contacts_page(page):
    """Contacts page object"""
    return ContactsPage(page)


@pytest.fixture
def logged_in_page(page, app_url, login_page):
    """Logged-in page (performs login before test)"""
    user = TEST_DATA["known_user"]
    login_page.login(user["email"], user["password"])
    yield page


@pytest.fixture(scope="session")
def api_token(app_url):
    return get_auth_token(app_url)


@pytest.fixture(scope="session", autouse=True)
def _reports_dir():
    REPORTS_DIR.mkdir(exist_ok=True)


# LOGGING (UI / API)
@pytest.fixture(scope="function", autouse=True)
def logger(request):
    test_type = "ui" if "ui" in request.keywords else "api"
    log_dir = REPORTS_DIR / "logs" / test_type
    log_dir.mkdir(parents=True, exist_ok=True)

    test_name = request.node.name
    log_file = log_dir / f"{test_name}.log"

    logger_instance = logging.getLogger(test_name)
    logger_instance.setLevel(logging.INFO)

    if logger_instance.hasHandlers():
        logger_instance.handlers.clear()

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    logger_instance.addHandler(file_handler)

    yield logger_instance
    file_handler.close()


# FAIL REPORTS (SCREENSHOTS FOR UI / JSON FOR API) WITH ALLURE ATTACHMENTS
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        timestamp = datetime.now().strftime("%H-%M-%S")

        # ---------- UI FAILURE ----------
        if "page" in item.fixturenames or "logged_in_page" in item.fixturenames:
            try:
                page_fixture_name = "page" if "page" in item.fixturenames else "logged_in_page"
                page = item.funcargs[page_fixture_name]

                screenshot_dir = REPORTS_DIR / "screenshots" / "failures"
                screenshot_dir.mkdir(parents=True, exist_ok=True)

                screenshot_path = screenshot_dir / f"{item.name}_{timestamp}.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                print(f"\n[!] UI Fail! Screenshot saved: {screenshot_path}")

                # ========== ALLURE ATTACH (UI) ==========
                with open(screenshot_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=f"Screenshot on failure ({timestamp})",
                        attachment_type=allure.attachment_type.PNG
                    )
                # ========================================

            except Exception as e:
                print(f"\n[!] Screenshot error: {e}")

        # ---------- API FAILURE ----------
        else:
            try:
                # Try to get response body from test context
                if "body" in item.funcargs or "body" in item.funcargs.get("request", {}).node.__dict__.get("funcargs", {}):
                    body = item.funcargs.get("body")
                else:
                    tb = call.excinfo._excinfo[2]
                    while tb.tb_next:
                        tb = tb.tb_next
                    body = tb.tb_frame.f_locals.get("body", None)

                if body:
                    api_fail_dir = REPORTS_DIR / "api_failures"
                    api_fail_dir.mkdir(parents=True, exist_ok=True)

                    json_path = api_fail_dir / f"{item.name}_{timestamp}.json"
                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(body, f, indent=4, ensure_ascii=False)
                    print(f"\n[!] API Fail! Error JSON saved: {json_path}")

                    # ========== ALLURE ATTACH (API) ==========
                    with open(json_path, "r", encoding="utf-8") as f:
                        allure.attach(
                            f.read(),
                            name=f"API response on failure ({timestamp})",
                            attachment_type=allure.attachment_type.JSON
                        )
                    # ==========================================

            except Exception as e:
                print(f"\n[!] API JSON save error: {e}")