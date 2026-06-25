from typing import Optional
from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        
        # locators
        self.LOGIN_EMAIL = 'input[placeholder="Enter your email"]'
        self.LOGIN_PASSWORD = 'input[placeholder="Enter your password"]'
        self.LOGIN_BUTTON = 'button:has-text("Login")'

        self.REGISTER_EMAIL = 'input[placeholder="Enter your email"]'
        self.REGISTER_PASSWORD = 'input[placeholder="Enter your password (min. 6 characters)"]'
        self.REGISTER_CONFIRM = 'input[placeholder="Confirm your password"]'
        self.REGISTER_BUTTON = 'button:has-text("Register")'

    # autorization methods
    def goto_login(self) -> None:
        url = self.base_url.rstrip("/") + "/"
        self.page.goto(url, wait_until="domcontentloaded", timeout=15000)

    def login(self, email: str, password: str) -> None:
        self.goto_login()
        self.page.fill(self.LOGIN_EMAIL, email)
        self.page.fill(self.LOGIN_PASSWORD, password)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_url("**/contacts", timeout=20000)
        self.page.get_by_role("heading", name="Contact List").wait_for(state="visible", timeout=15000)
        self.page.wait_for_function(
            """() => {
                return document.querySelector('h3')
                    || document.body.innerText.includes('No contacts yet');
            }""",
            timeout=15000,
        )

    def submit_login(self, email: str = "", password: str = "") -> None:
        if email:
            self.page.fill(self.LOGIN_EMAIL, email)
        if password:
            self.page.fill(self.LOGIN_PASSWORD, password)
        self.page.click(self.LOGIN_BUTTON)

    def try_login(self, email: str, password: str) -> None:
        self.goto_login()
        self.submit_login(email=email, password=password)
        self.page.wait_for_timeout(1000)

    def login_should_fail(self) -> None:
        assert "/contacts" not in self.page.url

    def get_login_email_locator(self):
        """return email locator for HTML validation"""
        return self.page.locator(self.LOGIN_EMAIL)

    # registration page methods
    def goto_register(self) -> None:
        url = self.base_url.rstrip("/") + "/register"
        self.page.goto(url, wait_until="domcontentloaded", timeout=15000)

    def submit_register(self, email: str, password: str, confirm: Optional[str] = None) -> None:
        self.page.fill(self.REGISTER_EMAIL, email)
        self.page.fill(self.REGISTER_PASSWORD, password)
        self.page.fill(self.REGISTER_CONFIRM, confirm if confirm is not None else password)
        self.page.click(self.REGISTER_BUTTON)

    def register_user(self, email: str, password: str) -> None:
        self.goto_register()
        self.submit_register(email, password)
        self.page.wait_for_function(
            "() => !window.location.pathname.includes('/register')",
            timeout=20000,
        )

    def get_url(self) -> str:
        """get browsers URL"""
        return self.page.url
