import json
import os
from pathlib import Path

#  config test_data.json
CONFIG_DIR = Path(__file__).parent
DATA_FILE_PATH = CONFIG_DIR / "test_data.json"

# automat  JSON
with open(DATA_FILE_PATH, "r", encoding="utf-8") as f:
    TEST_DATA = json.load(f)

# environment  URL
APP_URL = os.getenv("APP_URL", "https://qa-sendbox.org/")
BROWSER_TYPE = os.getenv("BROWSER_TYPE", "chromium")
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "True").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
