from typing import Optional
from playwright.sync_api import Locator, Page

class ContactsPage:
    def __init__(self, page: Page):
        self.page = page
        
        # locators
        self.NEW_CONTACT_BUTTON = 'button:has-text("New Contact")'
        self.CONTACT_NAME = 'input[placeholder="Enter contact name"]'
        self.CONTACT_EMAIL = 'input[placeholder="Enter email address"]'
        self.CONTACT_PHONE = 'input[placeholder="10-digit number"]'
        self.SAVE_CONTACT_BUTTON = 'button:has-text("Save Contact")'
        self.SEARCH_INPUT = 'input[placeholder="Search by name, email, or phone..."]'
        self.GROUP_FILTER_LABEL = "Group:"
        self.SORT_BY_LABEL = "Sort by:"
        self.CONTACT_MODAL = ".modal-overlay"

    # helpers
    def contact_heading(self, name: str) -> Locator:
        return self.page.locator("h3").filter(has_text=name).first

    def contact_card(self, contact_name: str) -> Locator:
        heading = self.contact_heading(contact_name)
        element_id = heading.get_attribute("id")
        if not element_id or not element_id.startswith("contact-name-"):
            raise ValueError(f"Contact heading id not found for: {contact_name}")
        suffix = element_id.removeprefix("contact-name-")
        return self.page.locator(f"#contact-card-{suffix}")

    def _click_card_button(self, contact_name: str, button_name: str) -> None:
        self.contact_card(contact_name).locator(f'button[title="{button_name}"]').click()

    # methods
    def logout(self) -> None:
        self.page.click('button:has-text("Logout")')
        self.page.wait_for_url(lambda url: "/contacts" not in url, timeout=15000)

    def open_new_contact_modal(self) -> None:
        self.page.click(self.NEW_CONTACT_BUTTON)
        self.page.wait_for_selector(self.CONTACT_NAME, state="visible", timeout=10000)

    def contact_modal(self) -> Locator:
        return self.page.locator(self.CONTACT_MODAL)

    def submit_contact_form(self) -> None:
        self.page.click(self.SAVE_CONTACT_BUTTON)

    def add_contact(self, name: str, phone: str, email: Optional[str] = None, group: Optional[str] = None) -> None:
        self.open_new_contact_modal()
        modal = self.contact_modal()
        modal.locator(self.CONTACT_NAME).fill(name)
        if email:
            modal.locator(self.CONTACT_EMAIL).fill(email)
        modal.locator(self.CONTACT_PHONE).fill(phone)
        if group:
            modal.get_by_role("combobox", name="Group").select_option(group)
        self.submit_contact_form()
        
        saving = self.page.locator('button:has-text("Saving...")')
        saving.wait_for(state="hidden", timeout=20000)
        self.page.locator(".modal-overlay").wait_for(state="hidden", timeout=20000)
        self.contact_heading(name).wait_for(state="visible", timeout=15000)

    def edit_contact_name(self, contact_name: str, new_name: str) -> None:
        self._click_card_button(contact_name, "Edit contact")
        self.page.wait_for_selector(self.CONTACT_NAME, state="visible", timeout=10000)
        self.page.fill(self.CONTACT_NAME, new_name)
        self.page.click(self.SAVE_CONTACT_BUTTON)
        self.page.locator(".modal-overlay").wait_for(state="hidden", timeout=20000)
        self.contact_heading(new_name).wait_for(state="visible", timeout=15000)

    def delete_contact(self, contact_name: str) -> None:
        def accept_dialog(dialog) -> None:
            dialog.accept()

        self.page.once("dialog", accept_dialog)
        self._click_card_button(contact_name, "Delete contact")
        self.contact_heading(contact_name).wait_for(state="hidden", timeout=15000)

    def search_contacts(self, query: str) -> None:
        self.page.fill(self.SEARCH_INPUT, query)

    def get_contact_names(self) -> list[str]:
        return self.page.locator("h3").all_text_contents()

    def filter_contacts_by_group(self, group_value: str) -> None:
        self.page.get_by_label(self.GROUP_FILTER_LABEL).select_option(group_value)

    def sort_contacts_by(self, sort_value: str) -> None:
        self.page.get_by_label(self.SORT_BY_LABEL).select_option(sort_value)

    def switch_contacts_view(self, view: str) -> None:
        label = "Grid view" if view == "grid" else "List view"
        self.page.get_by_role("button", name=label).click()

    def contacts_view_layout(self) -> str:
        return self.page.evaluate(
            """() => {
                const grid = document.querySelector('.contacts-grid');
                const list = document.querySelector('.contacts-list');
                if (grid && grid.offsetParent !== null) return 'grid';
                if (list && list.offsetParent !== null) return 'list';
                return '';
            }"""
        )

    def is_favorite_card(self, card: Locator) -> bool:
        remove_btn = card.locator('button[title="Remove from favorites"]')
        return remove_btn.count() > 0

    def add_contact_to_favorites(self, contact_name: str) -> None:
        card = self.contact_card(contact_name)
        card.locator('button[title="Add to favorites"]').click()
        card.locator('button[title="Remove from favorites"]').wait_for(state="visible", timeout=10000)
