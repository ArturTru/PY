import pytest
from playwright.sync_api import expect

from config.settings import TEST_DATA
from helpers.app_flows import (
    LOGIN_BUTTON,
    LOGIN_EMAIL,
    add_contact,
    contact_heading,
    get_contact_names,
    goto_login,
    login,
    logout,
    unique_contact_name,
)

pytestmark = pytest.mark.smoke


def test_tc_01_login_page(page, app_url):
    goto_login(page, app_url)
    assert page.get_by_role("heading", name="Contact List App").is_visible()
    assert page.locator(LOGIN_EMAIL).is_visible()
    assert page.locator(LOGIN_BUTTON).is_visible()


def test_tc_02_login(page, app_url):
    user = TEST_DATA["known_user"]
    login(page, app_url, user["email"], user["password"])
    assert "/contacts" in page.url


def test_tc_05_contacts_list(logged_in_page):
    assert logged_in_page.get_by_role("heading", name="Contact List").is_visible()
    assert get_contact_names(logged_in_page)


def test_tc_04_add_contact(logged_in_page):
    name = unique_contact_name("Smoke")
    add_contact(logged_in_page, name, "5554443322", email="smoke@example.com")
    assert contact_heading(logged_in_page, name).is_visible()


def test_tc_08_logout(page, app_url):
    user = TEST_DATA["known_user"]
    login(page, app_url, user["email"], user["password"])
    logout(page)
    expect(page.locator(LOGIN_BUTTON)).to_be_visible()
