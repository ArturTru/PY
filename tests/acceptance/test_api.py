import pytest

from helpers.api_client import api_request, create_contact, delete_contact
from helpers.app_flows import unique_email

pytestmark = [pytest.mark.acceptance, pytest.mark.api]


def test_contact_crud(app_url, api_token, logger):
    logger.info("START: test_contact_crud")
    
    name = f"API {unique_email('api')[-8:]}"
    logger.info(f"Create contact: {name}")
    contact_id = create_contact(app_url, api_token, name)
    logger.debug(f"Contact created. ID: {contact_id}")

    logger.info(f"GET contact ID: {contact_id}")
    status, body = api_request(app_url, f"/api/contacts/{contact_id}", token=api_token)
    logger.debug(f"Response: {status}, Body: {body}")
    
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("name") == name

    logger.info(f"PUT contact ID: {contact_id}")
    status, body = api_request(
        app_url,
        f"/api/contacts/{contact_id}",
        method="PUT",
        token=api_token,
        json_body={"comment": "updated"},
    )
    logger.debug(f"Response: {status}, Body: {body}")
    
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("comment") == "updated"

    logger.info(f"Delete contact ID: {contact_id}")
    delete_contact(app_url, api_token, contact_id)
    logger.info("FINISH: test_contact_crud SUCCESS")


def test_favorite_toggle(app_url, api_token, logger):
    logger.info("START: test_favorite_toggle")
    
    contact_name = f"Fav {unique_email('fav')[-8:]}"
    contact_id = create_contact(app_url, api_token, contact_name)
    logger.debug(f"Base contact ID: {contact_id}")
    
    try:
        logger.info("Step 1: Set favorite to true")
        status, body = api_request(
            app_url,
            f"/api/contacts/{contact_id}/favorite?is_favorite=true",
            method="PATCH",
            token=api_token,
        )
        logger.debug(f"Response: {status}, Body: {body}")
        assert status == 200
        assert isinstance(body, dict)
        assert body.get("is_favorite") is True

        logger.info("Step 2: Set favorite to false")
        status, body = api_request(
            app_url,
            f"/api/contacts/{contact_id}/favorite?is_favorite=false",
            method="PATCH",
            token=api_token,
        )
        logger.debug(f"Response: {status}, Body: {body}")
        assert status == 200
        assert isinstance(body, dict)
        assert body.get("is_favorite") is False
        
    finally:
        logger.info(f"Cleanup: Delete contact ID: {contact_id}")
        delete_contact(app_url, api_token, contact_id)
        logger.info("FINISH: test_favorite_toggle SUCCESS")