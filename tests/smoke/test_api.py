import pytest

from config.settings import TEST_DATA
from helpers.api_client import api_request

pytestmark = pytest.mark.smoke


def test_login_returns_token(app_url):
    user = TEST_DATA["known_user"]
    status, body = api_request(
        app_url,
        "/api/auth/login",
        method="POST",
        form_body={"username": user["email"], "password": user["password"]},
    )
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("token_type") == "bearer"
    assert body.get("access_token")


def test_me_with_token(app_url, api_token):
    status, body = api_request(app_url, "/api/auth/me", token=api_token)
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("email") == TEST_DATA["known_user"]["email"]


def test_contacts_need_auth(app_url):
    status, _ = api_request(app_url, "/api/contacts")
    assert status in (401, 403)
