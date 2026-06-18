import pytest

from config.settings import TEST_DATA
from helpers.app_flows import (
    CONTACT_NAME,
    LOGIN_EMAIL,
    add_contact,
    add_contact_to_favorites,
    contact_card,
    contact_heading,
    contact_modal,
    contacts_view_layout,
    delete_contact,
    edit_contact_name,
    filter_contacts_by_group,
    get_contact_names,
    goto_register,
    is_favorite_card,
    login,
    login_should_fail,
    open_new_contact_modal,
    register_user,
    search_contacts,
    sort_contacts_by,
    submit_contact_form,
    submit_register,
    switch_contacts_view,
    try_login,
    unique_contact_name,
    unique_email,
)

pytestmark = pytest.mark.acceptance


def test_tc_03_register_and_login(page, app_url):
    email = unique_email("reg")
    password = TEST_DATA["registration_password"]
    register_user(page, app_url, email, password)
    login(page, app_url, email, password)
    assert "/contacts" in page.url


def test_tc_06_edit_contact(logged_in_page):
    old_name = unique_contact_name("Edit")
    new_name = unique_contact_name("Edited")
    add_contact(logged_in_page, old_name, "5553332211")
    edit_contact_name(logged_in_page, old_name, new_name)
    assert contact_heading(logged_in_page, new_name).is_visible()


def test_tc_07_delete_contact(logged_in_page):
    name = unique_contact_name("Del")
    add_contact(logged_in_page, name, "5552221100")
    delete_contact(logged_in_page, name)
    assert contact_heading(logged_in_page, name).count() == 0


def test_tc_09_wrong_password(page, app_url):
    user = TEST_DATA["known_user"]
    try_login(page, app_url, user["email"], "WrongPassword999")
    login_should_fail(page)


def test_tc_10_unknown_user(page, app_url):
    try_login(page, app_url, unique_email("ghost"), "TestPass123")
    login_should_fail(page)


def test_tc_11_empty_login(page, app_url):
    try_login(page, app_url, "", "")
    login_should_fail(page)
    assert page.locator(LOGIN_EMAIL).is_visible()
    assert not page.locator(LOGIN_EMAIL).evaluate("el => el.checkValidity()")


def test_tc_12_register_existing_email(page, app_url):
    user = TEST_DATA["known_user"]
    goto_register(page, app_url)
    submit_register(page, user["email"], TEST_DATA["registration_password"])
    page.wait_for_function(
        "() => window.location.pathname.includes('/register')",
        timeout=5000,
    )
    assert "/register" in page.url


def test_tc_13_password_mismatch(page, app_url):
    goto_register(page, app_url)
    submit_register(
        page,
        unique_email("mismatch"),
        password="TestPass123",
        confirm="OtherPass456",
    )
    page.wait_for_timeout(1000)
    assert "/register" in page.url


def test_tc_14_contact_without_required_fields(logged_in_page):
    before = len(get_contact_names(logged_in_page))
    open_new_contact_modal(logged_in_page)
    submit_contact_form(logged_in_page)
    assert contact_modal(logged_in_page).is_visible()
    assert logged_in_page.locator(CONTACT_NAME).is_visible()
    assert len(get_contact_names(logged_in_page)) == before


def test_tc_15_bad_email_on_register(page, app_url):
    goto_register(page, app_url)
    submit_register(page, "notanemail", password="TestPass123", confirm="TestPass123")
    page.wait_for_timeout(1000)
    assert "/register" in page.url


def test_tc_16_search(logged_in_page):
    name = unique_contact_name("Search")
    add_contact(logged_in_page, name, "5557778899")
    search_contacts(logged_in_page, name)
    assert contact_heading(logged_in_page, name).is_visible()


def test_tc_17_sort_by_favorite(logged_in_page):
    name = unique_contact_name("Fav")
    add_contact(logged_in_page, name, "5556667788")
    add_contact_to_favorites(logged_in_page, name)

    sort_contacts_by(logged_in_page, "is_favorite")
    logged_in_page.wait_for_timeout(500)
    assert logged_in_page.get_by_label("Sort by:").input_value() == "is_favorite"
    assert is_favorite_card(contact_card(logged_in_page, name))


def test_tc_18_filter_by_group(logged_in_page):
    name = unique_contact_name("Work")
    add_contact(logged_in_page, name, "5551110099", group="work")
    filter_contacts_by_group(logged_in_page, "work")
    logged_in_page.wait_for_timeout(500)
    assert contact_heading(logged_in_page, name).is_visible()
    filter_contacts_by_group(logged_in_page, "friends")
    logged_in_page.wait_for_timeout(500)
    assert name not in get_contact_names(logged_in_page)


def test_tc_19_switch_view(logged_in_page):
    switch_contacts_view(logged_in_page, "list")
    assert contacts_view_layout(logged_in_page) == "list"
    switch_contacts_view(logged_in_page, "grid")
    assert contacts_view_layout(logged_in_page) == "grid"


def test_tc_20_swagger(page, app_url):
    page.goto(f"{app_url.rstrip('/')}/api/docs", wait_until="domcontentloaded", timeout=15000)
    html = page.content().lower()
    assert "swagger" in html or "openapi" in html
