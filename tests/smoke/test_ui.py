import pytest
from playwright.sync_api import expect

from config.settings import TEST_DATA
# Импортируем только генератор данных из хелперов
from helpers.app_flows import unique_contact_name

pytestmark = [pytest.mark.smoke, pytest.mark.ui]


def test_tc_01_login_page(login_page, logger):
    logger.info("START: test_tc_01_login_page")
    
    logger.info("Navigate to login page")
    login_page.goto_login()
    
    logger.info("Verify login page elements are visible")
    assert login_page.page.get_by_role("heading", name="Contact List App").is_visible()
    assert login_page.page.locator(login_page.LOGIN_EMAIL).is_visible()
    assert login_page.page.locator(login_page.LOGIN_BUTTON).is_visible()
    
    logger.info("FINISH: test_tc_01_login_page SUCCESS")


def test_tc_02_login(login_page, logger):
    logger.info("START: test_tc_02_login")
    
    user = TEST_DATA["known_user"]
    logger.info(f"Login as user: {user['email']}")
    login_page.login(user["email"], user["password"])
    
    logger.info("Verify redirect to contacts page")
    logger.debug(f"Current URL: {login_page.get_url()}")
    assert "/contacts" in login_page.get_url()
    
    logger.info("FINISH: test_tc_02_login SUCCESS")


def test_tc_05_contacts_list(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_05_contacts_list")
    
    logger.info("Verify Contact List heading is visible")
    assert logged_in_page.get_by_role("heading", name="Contact List").is_visible()
    
    logger.info("Fetch and verify contact names from list")
    names = contacts_page.get_contact_names()
    logger.debug(f"Found contacts: {names}")
    assert names
    
    logger.info("FINISH: test_tc_05_contacts_list SUCCESS")


def test_tc_04_add_contact(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_04_add_contact")
    
    name = unique_contact_name("Smoke")
    logger.info(f"Adding new contact: {name}")
    contacts_page.add_contact(name, "5554443322", email="smoke@example.com")
    
    logger.info("Verify new contact heading is visible")
    assert contacts_page.contact_heading(name).is_visible()
    
    logger.info("FINISH: test_tc_04_add_contact SUCCESS")


def test_tc_08_logout(login_page, contacts_page, logger):
    logger.info("START: test_tc_08_logout")
    
    user = TEST_DATA["known_user"]
    logger.info(f"Login as user: {user['email']}")
    login_page.login(user["email"], user["password"])
    
    logger.info("Perform logout")
    contacts_page.logout()
    
    logger.info("Verify login button is visible after logout")
    expect(login_page.page.locator(login_page.LOGIN_BUTTON)).to_be_visible()
    
    logger.info("FINISH: test_tc_08_logout SUCCESS")
