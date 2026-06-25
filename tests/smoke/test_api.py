import pytest

from config.settings import TEST_DATA
from helpers.api_client import api_request

pytestmark = [pytest.mark.smoke, pytest.mark.api]


def test_login_returns_token(app_url, logger):
    logger.info("START: test_login_returns_token")
    
    user = TEST_DATA["known_user"]
    logger.info(f"Send POST login request for user: {user['email']}")
    
    status, body = api_request(
        app_url,
        "/api/auth/login",
        method="POST",
        form_body={"username": user["email"], "password": user["password"]},
    )
    logger.debug(f"Response status: {status}")
    
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("token_type") == "bearer"
    assert body.get("access_token")
    
    logger.info("FINISH: test_login_returns_token SUCCESS")


def test_me_with_token(app_url, api_token, logger):
    logger.info("START: test_me_with_token")
    
    logger.info("Send GET request to /api/auth/me with token")
    status, body = api_request(app_url, "/api/auth/me", token=api_token)
    logger.debug(f"Response status: {status}, Body: {body}")
    
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("email") == TEST_DATA["known_user"]["email"]
    
    logger.info("FINISH: test_me_with_token SUCCESS")


def test_contacts_need_auth(app_url, logger):
    logger.info("START: test_contacts_need_auth")
    
    logger.info("Send GET request to /api/contacts without token")
    status, _ = api_request(app_url, "/api/contacts")
    logger.debug(f"Response status: {status}")
    
    assert status in (401, 403)
    
    logger.info("FINISH: test_contacts_need_auth SUCCESS")
