import pytest
from config.settings import TEST_DATA
from helpers.api_client import api_request


@pytest.mark.smoke
@pytest.mark.api
def test_login_returns_token(app_url, logger):
    """Verify login"""
    logger.info("START: test_login_returns_token")
    user = TEST_DATA["known_user"]
    logger.info(f"POST login for: {user['email']}")

    status, body = api_request(
        app_url,
        "/api/auth/login",
        method="POST",
        form_body={"username": user["email"], "password": user["password"]},
    )
    logger.debug(f"Response status: {status}")

    assert status == 200, f"Login failed, status {status}"
    assert isinstance(body, dict), "Response is not dict"
    assert body.get("token_type") == "bearer", "Invalid token_type"
    assert body.get("access_token"), "Missing access_token"

    logger.info("FINISH: test_login_returns_token SUCCESS")


@pytest.mark.smoke
@pytest.mark.api
def test_me_with_token(app_url, api_token, logger):
    """Verify returns correct token."""
    logger.info("START: test_me_with_token")
    logger.info("GET /api/auth/me with token")

    status, body = api_request(app_url, "/api/auth/me", token=api_token)
    logger.debug(f"Status: {status}, Body: {body}")

    assert status == 200, f"GET /me failed, status {status}"
    assert isinstance(body, dict), "Response is not dict"
    expected = TEST_DATA["known_user"]["email"]
    assert body.get("email") == expected, f"Expected {expected}, got {body.get('email')}"

    logger.info("FINISH: test_me_with_token SUCCESS")


@pytest.mark.smoke
@pytest.mark.api
def test_contacts_need_auth(app_url, logger):
    """Verify /contacts without token returns 401 or 403."""
    logger.info("START: test_contacts_need_auth")
    logger.info("GET /api/contacts without token")

    status, _ = api_request(app_url, "/api/contacts")
    logger.debug(f"Status: {status}")

    assert status in (401, 403), f"Expected 401/403, got {status}"

    logger.info("FINISH: test_contacts_need_auth SUCCESS")
    