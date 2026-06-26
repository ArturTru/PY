import pytest
from helpers.api_client import api_request, create_contact, delete_contact
from helpers.app_flows import unique_email



@pytest.mark.api
@pytest.mark.crud
@pytest.mark.regression
def test_contact_crud(app_url, api_token, logger):
 
    logger.info("START: test_contact_crud")

    name = f"API {unique_email('api')[-8:]}"
    logger.info(f"Create contact: {name}")
    contact_id = create_contact(app_url, api_token, name)
    logger.debug(f"Contact created. ID: {contact_id}")

    # GET 
    logger.info(f"GET contact ID: {contact_id}")
    status, body = api_request(app_url, f"/api/contacts/{contact_id}", token=api_token)
    assert status == 200, f"GET failed with status {status}"
    assert isinstance(body, dict), "Response body is not a dict"
    assert body.get("name") == name, f"Expected name '{name}', got '{body.get('name')}'"
    logger.info("GET successful, name matches")

    
    logger.info(f"PUT contact ID: {contact_id}")
    status, body = api_request(
        app_url,
        f"/api/contacts/{contact_id}",
        method="PUT",
        token=api_token,
        json_body={"comment": "updated"},
    )
    assert status == 200, f"PUT failed with status {status}"
    assert isinstance(body, dict), "Response body is not a dict"
    assert body.get("comment") == "updated", "Comment not updated"
    logger.info("PUT successful, comment updated")

    
    logger.info(f"DELETE contact ID: {contact_id}")
    delete_contact(app_url, api_token, contact_id)
    status, _ = api_request(app_url, f"/api/contacts/{contact_id}", token=api_token)
    assert status == 404, f"Contact still exists after deletion, status {status}"

    logger.info("FINISH: test_contact_crud SUCCESS")


@pytest.mark.api
@pytest.mark.favorite
@pytest.mark.regression
def test_favorite_toggle(app_url, api_token, logger):
    
    logger.info("START: test_favorite_toggle")

    contact_name = f"Fav {unique_email('fav')[-8:]}"
    contact_id = create_contact(app_url, api_token, contact_name)
    logger.debug(f"Base contact ID: {contact_id}")

    try:
        #  favorite = true
        logger.info("Step 1: Set favorite to true")
        status, body = api_request(
            app_url,
            f"/api/contacts/{contact_id}/favorite?is_favorite=true",
            method="PATCH",
            token=api_token,
        )
        assert status == 200, f"PATCH favorite=true failed with status {status}"
        assert isinstance(body, dict), "Response body is not a dict"
        assert body.get("is_favorite") is True, "Favorite is not True after setting to true"
        logger.info("Favorite set to true verified")

        # favorite = false
        logger.info("Step 2: Set favorite to false")
        status, body = api_request(
            app_url,
            f"/api/contacts/{contact_id}/favorite?is_favorite=false",
            method="PATCH",
            token=api_token,
        )
        assert status == 200, f"PATCH favorite=false failed with status {status}"
        assert isinstance(body, dict), "Response body is not a dict"
        assert body.get("is_favorite") is False, "Favorite is not False after setting to false"
        logger.info("Favorite set to false verified")

    finally:
        logger.info(f"Cleanup: Delete contact ID: {contact_id}")
        delete_contact(app_url, api_token, contact_id)
        logger.info("FINISH: test_favorite_toggle SUCCESS")