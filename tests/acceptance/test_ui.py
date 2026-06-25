import pytest

from config.settings import TEST_DATA
# From helper generattors
from helpers.app_flows import unique_contact_name, unique_email

pytestmark = [pytest.mark.acceptance, pytest.mark.ui]


def test_tc_03_register_and_login(login_page, page, logger):
    logger.info("START: test_tc_03_register_and_login")
    email = unique_email("reg")
    password = TEST_DATA["registration_password"]
    
    logger.info(f"Register new user: {email}")
    login_page.register_user(email, password)
    
    logger.info("Login with new credentials")
    login_page.login(email, password)
    
    logger.info("Verify redirect to contacts page")
    assert "/contacts" in page.url
    logger.info("FINISH: test_tc_03_register_and_login SUCCESS")


def test_tc_06_edit_contact(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_06_edit_contact")
    old_name = unique_contact_name("Edit")
    new_name = unique_contact_name("Edited")
    
    logger.info(f"Add contact: {old_name}")
    contacts_page.add_contact(old_name, "5553332211")
    
    logger.info(f"Edit contact name to: {new_name}")
    contacts_page.edit_contact_name(old_name, new_name)
    
    logger.info("Verify new name is visible")
    assert contacts_page.contact_heading(new_name).is_visible()
    logger.info("FINISH: test_tc_06_edit_contact SUCCESS")


def test_tc_07_delete_contact(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_07_delete_contact")
    name = unique_contact_name("Del")
    
    logger.info(f"Add contact: {name}")
    contacts_page.add_contact(name, "5552221100")
    
    logger.info(f"Delete contact: {name}")
    contacts_page.delete_contact(name)
    
    logger.info("Verify contact is removed from layout")
    assert contacts_page.contact_heading(name).count() == 0
    logger.info("FINISH: test_tc_07_delete_contact SUCCESS")


def test_tc_09_wrong_password(login_page, logger):
    logger.info("START: test_tc_09_wrong_password")
    user = TEST_DATA["known_user"]
    
    logger.info(f"Try login with wrong password for user: {user['email']}")
    login_page.try_login(user["email"], "WrongPassword999")
    
    logger.info("Verify login failed error")
    login_page.login_should_fail()
    logger.info("FINISH: test_tc_09_wrong_password SUCCESS")


def test_tc_10_unknown_user(login_page, logger):
    logger.info("START: test_tc_10_unknown_user")
    ghost_email = unique_email("ghost")
    
    logger.info(f"Try login as non-existing user: {ghost_email}")
    login_page.try_login(ghost_email, "TestPass123")
    
    logger.info("Verify login failed error")
    login_page.login_should_fail()
    logger.info("FINISH: test_tc_10_unknown_user SUCCESS")


def test_tc_11_empty_login(login_page, page, logger):
    logger.info("START: test_tc_11_empty_login")
    
    logger.info("Try login with empty fields")
    login_page.try_login("", "")
    
    logger.info("Verify login page rules and HTML validation")
    login_page.login_should_fail()
    
    email_loc = login_page.get_login_email_locator()
    assert email_loc.is_visible()
    assert not email_loc.evaluate("el => el.checkValidity()")
    logger.info("FINISH: test_tc_11_empty_login SUCCESS")


def test_tc_12_register_existing_email(login_page, logger):
    logger.info("START: test_tc_12_register_existing_email")
    user = TEST_DATA["known_user"]
    
    logger.info(f"Navigate to registration and submit existing email: {user['email']}")
    login_page.goto_register()
    login_page.submit_register(user["email"], TEST_DATA["registration_password"])
    
    logger.info("Verify stay on register page")
    login_page.page.wait_for_function(
        "() => window.location.pathname.includes('/register')",
        timeout=5000,
    )
    assert "/register" in login_page.get_url()
    logger.info("FINISH: test_tc_12_register_existing_email SUCCESS")


def test_tc_13_password_mismatch(login_page, logger):
    logger.info("START: test_tc_13_password_mismatch")
    
    logger.info("Submit registration form with mismatched passwords")
    login_page.goto_register()
    login_page.submit_register(
        unique_email("mismatch"),
        password="TestPass123",
        confirm="OtherPass456",
    )
    login_page.page.wait_for_timeout(1000)
    
    logger.info("Verify stay on register page due to mismatch")
    assert "/register" in login_page.get_url()
    logger.info("FINISH: test_tc_13_password_mismatch SUCCESS")


def test_tc_14_contact_without_required_fields(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_14_contact_without_required_fields")
    
    logger.info("Check initial contacts list length")
    before = len(contacts_page.get_contact_names())
    logger.debug(f"Initial contact count: {before}")
    
    logger.info("Open contact form modal and submit empty form")
    contacts_page.open_new_contact_modal()
    contacts_page.submit_contact_form()
    
    logger.info("Verify modal stays open and contact list count didn't change")
    assert contacts_page.contact_modal().is_visible()
    assert logged_in_page.locator(contacts_page.CONTACT_NAME).is_visible()
    assert len(contacts_page.get_contact_names()) == before
    logger.info("FINISH: test_tc_14_contact_without_required_fields SUCCESS")


def test_tc_15_bad_email_on_register(login_page, logger):
    logger.info("START: test_tc_15_bad_email_on_register")
    
    logger.info("Submit registration with invalid email pattern")
    login_page.goto_register()
    login_page.submit_register("notanemail", password="TestPass123", confirm="TestPass123")
    login_page.page.wait_for_timeout(1000)
    
    logger.info("Verify stay on register page")
    assert "/register" in login_page.get_url()
    logger.info("FINISH: test_tc_15_bad_email_on_register SUCCESS")


def test_tc_16_search(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_16_search")
    name = unique_contact_name("Search")
    
    logger.info(f"Add contact to search for: {name}")
    contacts_page.add_contact(name, "5557778899")
    
    logger.info(f"Perform search query for name: {name}")
    contacts_page.search_contacts(name)
    
    logger.info("Verify matched contact is visible")
    assert contacts_page.contact_heading(name).is_visible()
    logger.info("FINISH: test_tc_16_search SUCCESS")


def test_tc_17_sort_by_favorite(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_17_sort_by_favorite")
    name = unique_contact_name("Fav")
    
    logger.info(f"Add contact and set to favorites: {name}")
    contacts_page.add_contact(name, "5556667788")
    contacts_page.add_contact_to_favorites(name)

    logger.info("Sort contacts list by favorite parameter")
    contacts_page.sort_contacts_by("is_favorite")
    contacts_page.page.wait_for_timeout(500)
    
    logger.info("Verify sorting dropdown state and card styling")
    assert contacts_page.page.get_by_label(contacts_page.SORT_BY_LABEL).input_value() == "is_favorite"
    assert contacts_page.is_favorite_card(contacts_page.contact_card(name))
    logger.info("FINISH: test_tc_17_sort_by_favorite SUCCESS")


def test_tc_18_filter_by_group(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_18_filter_by_group")
    name = unique_contact_name("Work")
    
    logger.info(f"Add contact to 'work' group: {name}")
    contacts_page.add_contact(name, "5551110099", group="work")
    
    logger.info("Apply 'work' filter group")
    contacts_page.filter_contacts_by_group("work")
    contacts_page.page.wait_for_timeout(500)
    assert contacts_page.contact_heading(name).is_visible()
    
    logger.info("Apply 'friends' filter group")
    contacts_page.filter_contacts_by_group("friends")
    contacts_page.page.wait_for_timeout(500)
    
    contacts_page.contact_heading(name).wait_for(state="hidden", timeout=5000)
    
    logger.info("Verify 'work' contact disappeared from layout")
    assert name not in contacts_page.get_contact_names()
    logger.info("FINISH: test_tc_18_filter_by_group SUCCESS")



def test_tc_19_switch_view(logged_in_page, contacts_page, logger):
    logger.info("START: test_tc_19_switch_view")
    
    logger.info("Switch application layout view to 'list'")
    contacts_page.switch_contacts_view("list")
    assert contacts_page.contacts_view_layout() == "list"
    
    logger.info("Switch application layout view to 'grid'")
    contacts_page.switch_contacts_view("grid")
    assert contacts_page.contacts_view_layout() == "grid"
    logger.info("FINISH: test_tc_19_switch_view SUCCESS")


def test_tc_20_swagger(page, app_url, logger):
    logger.info("START: test_tc_20_swagger")
    target_url = f"{app_url.rstrip('/')}/api/docs"
    
    logger.info(f"Navigate to Swagger documentation URL: {target_url}")
    page.goto(target_url, wait_until="domcontentloaded", timeout=15000)
    
    logger.info("Verify page source context includes openapi definitions")
    html = page.content().lower()
    assert "swagger" in html or "openapi" in html
    logger.info("FINISH: test_tc_20_swagger SUCCESS")
