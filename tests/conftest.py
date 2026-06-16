# pylint: disable=redefined-outer-name

from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from config.settings import APP_URL, BROWSER_TYPE, HEADLESS_MODE, SLOW_MO, TEST_DATA
from helpers.api_client import get_auth_token
from helpers.app_flows import login

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


@pytest.fixture
def logged_in_page(page, app_url):
    user = TEST_DATA["known_user"]
    login(page, app_url, user["email"], user["password"])
    yield page


@pytest.fixture(scope="session")
def api_token(app_url):
    return get_auth_token(app_url)


@pytest.fixture(scope="session", autouse=True)
def _reports_dir():
    REPORTS_DIR.mkdir(exist_ok=True)
