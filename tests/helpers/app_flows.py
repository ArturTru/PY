import uuid
from typing import Optional

from playwright.sync_api import Locator, Page

LOGIN_EMAIL = 'input[placeholder="Enter your email"]'
LOGIN_PASSWORD = 'input[placeholder="Enter your password"]'
LOGIN_BUTTON = 'button:has-text("Login")'

REGISTER_EMAIL = 'input[placeholder="Enter your email"]'
REGISTER_PASSWORD = 'input[placeholder="Enter your password (min. 6 characters)"]'
REGISTER_CONFIRM = 'input[placeholder="Confirm your password"]'
REGISTER_BUTTON = 'button:has-text("Register")'

NEW_CONTACT_BUTTON = 'button:has-text("New Contact")'
CONTACT_NAME = 'input[placeholder="Enter contact name"]'
CONTACT_EMAIL = 'input[placeholder="Enter email address"]'
CONTACT_PHONE = 'input[placeholder="10-digit number"]'
SAVE_CONTACT_BUTTON = 'button:has-text("Save Contact")'
SEARCH_INPUT = 'input[placeholder="Search by name, email, or phone..."]'
GROUP_FILTER_LABEL = "Group:"
SORT_BY_LABEL = "Sort by:"
CONTACT_MODAL = ".modal-overlay"


def unique_email(prefix: str = "autotest") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}@example.com"


def unique_contact_name(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:6]}"


def goto_login(page: Page, base_url: str) -> None:
    url = base_url.rstrip("/") + "/"
    page.goto(url, wait_until="domcontentloaded", timeout=15000)


def login(page: Page, base_url: str, email: str, password: str) -> None:
    goto_login(page, base_url)
    page.fill(LOGIN_EMAIL, email)
    page.fill(LOGIN_PASSWORD, password)
    page.click(LOGIN_BUTTON)
    page.wait_for_url("**/contacts", timeout=20000)
    page.get_by_role("heading", name="Contact List").wait_for(
        state="visible", timeout=15000
    )
    page.wait_for_function(
        """() => {
            return document.querySelector('h3')
                || document.body.innerText.includes('No contacts yet');
        }""",
        timeout=15000,
    )


def goto_register(page: Page, base_url: str) -> None:
    url = base_url.rstrip("/") + "/register"
    page.goto(url, wait_until="domcontentloaded", timeout=15000)


def submit_register(
    page: Page, email: str, password: str, confirm: Optional[str] = None
) -> None:
    page.fill(REGISTER_EMAIL, email)
    page.fill(REGISTER_PASSWORD, password)
    page.fill(REGISTER_CONFIRM, confirm if confirm is not None else password)
    page.click(REGISTER_BUTTON)


def register_user(page: Page, base_url: str, email: str, password: str) -> None:
    goto_register(page, base_url)
    submit_register(page, email, password)
    page.wait_for_function(
        "() => !window.location.pathname.includes('/register')",
        timeout=20000,
    )


def submit_login(page: Page, email: str = "", password: str = "") -> None:
    if email:
        page.fill(LOGIN_EMAIL, email)
    if password:
        page.fill(LOGIN_PASSWORD, password)
    page.click(LOGIN_BUTTON)


def logout(page: Page) -> None:
    page.click('button:has-text("Logout")')
    page.wait_for_url(lambda url: "/contacts" not in url, timeout=15000)


def try_login(page: Page, base_url: str, email: str, password: str) -> None:
    goto_login(page, base_url)
    submit_login(page, email=email, password=password)
    page.wait_for_timeout(1000)


def login_should_fail(page: Page) -> None:
    assert "/contacts" not in page.url


def open_new_contact_modal(page: Page) -> None:
    page.click(NEW_CONTACT_BUTTON)
    page.wait_for_selector(CONTACT_NAME, state="visible", timeout=10000)


def contact_modal(page: Page):
    return page.locator(CONTACT_MODAL)


def submit_contact_form(page: Page) -> None:
    page.click(SAVE_CONTACT_BUTTON)


def add_contact(
    page: Page,
    name: str,
    phone: str,
    email: Optional[str] = None,
    group: Optional[str] = None,
) -> None:
    open_new_contact_modal(page)
    modal = contact_modal(page)
    modal.locator(CONTACT_NAME).fill(name)
    if email:
        modal.locator(CONTACT_EMAIL).fill(email)
    modal.locator(CONTACT_PHONE).fill(phone)
    if group:
        modal.get_by_role("combobox", name="Group").select_option(group)
    submit_contact_form(page)
    saving = page.locator('button:has-text("Saving...")')
    saving.wait_for(state="hidden", timeout=20000)
    page.locator(".modal-overlay").wait_for(state="hidden", timeout=20000)
    contact_heading(page, name).wait_for(state="visible", timeout=15000)


def contact_heading(page: Page, name: str):
    return page.locator("h3").filter(has_text=name).first


def edit_contact_name(page: Page, contact_name: str, new_name: str) -> None:
    _click_card_button(page, contact_name, "Edit contact")
    page.wait_for_selector(CONTACT_NAME, state="visible", timeout=10000)
    page.fill(CONTACT_NAME, new_name)
    page.click(SAVE_CONTACT_BUTTON)
    page.locator(".modal-overlay").wait_for(state="hidden", timeout=20000)
    contact_heading(page, new_name).wait_for(state="visible", timeout=15000)


def delete_contact(page: Page, contact_name: str) -> None:
    def accept_dialog(dialog) -> None:
        dialog.accept()

    page.once("dialog", accept_dialog)
    _click_card_button(page, contact_name, "Delete contact")
    contact_heading(page, contact_name).wait_for(state="hidden", timeout=15000)


def search_contacts(page: Page, query: str) -> None:
    page.fill(SEARCH_INPUT, query)


def get_contact_names(page: Page) -> list[str]:
    return page.locator("h3").all_text_contents()


def filter_contacts_by_group(page: Page, group_value: str) -> None:
    page.get_by_label(GROUP_FILTER_LABEL).select_option(group_value)


def sort_contacts_by(page: Page, sort_value: str) -> None:
    page.get_by_label(SORT_BY_LABEL).select_option(sort_value)


def switch_contacts_view(page: Page, view: str) -> None:
    label = "Grid view" if view == "grid" else "List view"
    page.get_by_role("button", name=label).click()


def contacts_view_layout(page: Page) -> str:
    layout = page.evaluate(
        """() => {
            const grid = document.querySelector('.contacts-grid');
            const list = document.querySelector('.contacts-list');
            if (grid && grid.offsetParent !== null) return 'grid';
            if (list && list.offsetParent !== null) return 'list';
            return '';
        }"""
    )
    return layout


def first_contact_card(page: Page) -> Locator:
    return page.locator('[id^="contact-card-"]').first


def is_favorite_card(card: Locator) -> bool:
    remove_btn = card.locator('button[title="Remove from favorites"]')
    return remove_btn.count() > 0


def contact_card(page: Page, contact_name: str) -> Locator:
    heading = page.locator("h3", has_text=contact_name).first
    element_id = heading.get_attribute("id")
    if not element_id or not element_id.startswith("contact-name-"):
        raise ValueError(f"Contact heading id not found for: {contact_name}")
    suffix = element_id.removeprefix("contact-name-")
    return page.locator(f"#contact-card-{suffix}")


def add_contact_to_favorites(page: Page, contact_name: str) -> None:
    card = contact_card(page, contact_name)
    card.locator('button[title="Add to favorites"]').click()
    card.locator('button[title="Remove from favorites"]').wait_for(
        state="visible", timeout=10000
    )


def _click_card_button(page: Page, contact_name: str, button_name: str) -> None:
    contact_card(page, contact_name).locator(f'button[title="{button_name}"]').click()
