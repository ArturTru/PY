import os

APP_URL = os.getenv("APP_URL", "https://qa-sendbox.org/")
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

TEST_DATA = {
    "known_user": {
        "email": "testuser@example.com",
        "password": "Test1234",
    },
    "registration_password": "TestPass123!",
}
