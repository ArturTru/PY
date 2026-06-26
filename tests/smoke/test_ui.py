import pytest
from playwright.sync_api import expect

from config.settings import TEST_DATA
from helpers.app_flows import unique_contact_name


@pytest.mark.smoke
@pytest.mark.ui
def test_tc_01_login_page(login_page, logger):
    """Verify login page elements are visible."""
    logger.info("START: test_tc_01_login_page")
    login_page.goto_login()

    assert login_page.page.get_by_role("heading", name="Contact List App").is_visible(), "Heading missing"
    assert login_page.page.locator(login_page.LOGIN_EMAIL).is_visible(), "Email field missing"
    assert login_page.page.locator(login_page.LOGIN_BUTTON).is_visible(), "Login button missing"

    logger.info("FINISH: test_tc_01_login_page SUCCESS")


@pytest.mark.smoke
@pytest.mark.ui
def test_tc_02_login(login_page, logger):
    """Verify login redirects to /contacts."""
    logger.info("START: test_tc_02_login")
    user = TEST_DATA["known_user"]
    logger.info(f"Login as: {user['email']}")
    login_page.login(user["email"], user["password"])

    assert "/contacts" in login_page.get_url(), "Not redirected to /contacts"

    logger.info("FINISH: test_tc_02_login SUCCESS")


@pytest.mark.smoke
@pytest.mark.ui
def test_tc_05_contacts_list(logged_in_page, contacts_page, logger):
    """Verify contacts list loads and shows contacts."""
    logger.info("START: test_tc_05_contacts_list")
    assert logged_in_page.get_by_role("heading", name="Contact List").is_visible(), "Contact List heading missing"

    names = contacts_page.get_contact_names()
    logger.debug(f"Contacts found: {names}")
    assert names, "No contacts found"

    logger.info("FINISH: test_tc_05_contacts_list SUCCESS")


@pytest.mark.smoke
@pytest.mark.ui
def test_tc_04_add_contact(logged_in_page, contacts_page, logger):
    """Verify adding a new contact works."""
    logger.info("START: test_tc_04_add_contact")
    name = unique_contact_name("Smoke")
    logger.info(f"Add contact: {name}")
    contacts_page.add_contact(name, "5554443322", email="smoke@example.com")

    assert contacts_page.contact_heading(name).is_visible(), f"Contact {name} not visible after add"

    logger.info("FINISH: test_tc_04_add_contact SUCCESS")


@pytest.mark.smoke
@pytest.mark.ui
def test_tc_08_logout(login_page, contacts_page, logger):
    """Verify logout redirects to login page."""
    logger.info("START: test_tc_08_logout")
    user = TEST_DATA["known_user"]
    logger.info(f"Login as: {user['email']}")
    login_page.login(user["email"], user["password"])

    logger.info("Logout")
    contacts_page.logout()

    expect(login_page.page.locator(login_page.LOGIN_BUTTON)).to_be_visible()
    logger.info("FINISH: test_tc_08_logout SUCCESS")
    