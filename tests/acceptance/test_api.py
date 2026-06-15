import pytest

from helpers.api_client import api_request, create_contact, delete_contact
from helpers.app_flows import unique_email

pytestmark = pytest.mark.acceptance


def test_contact_crud(app_url, api_token):
    name = f"API {unique_email('api')[-8:]}"
    contact_id = create_contact(app_url, api_token, name)

    status, body = api_request(app_url, f"/api/contacts/{contact_id}", token=api_token)
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("name") == name

    status, body = api_request(
        app_url,
        f"/api/contacts/{contact_id}",
        method="PUT",
        token=api_token,
        json_body={"comment": "updated"},
    )
    assert status == 200
    assert isinstance(body, dict)
    assert body.get("comment") == "updated"

    delete_contact(app_url, api_token, contact_id)


def test_favorite_toggle(app_url, api_token):
    contact_id = create_contact(app_url, api_token, f"Fav {unique_email('fav')[-8:]}")
    try:
        status, body = api_request(
            app_url,
            f"/api/contacts/{contact_id}/favorite?is_favorite=true",
            method="PATCH",
            token=api_token,
        )
        assert status == 200
        assert isinstance(body, dict)
        assert body.get("is_favorite") is True

        status, body = api_request(
            app_url,
            f"/api/contacts/{contact_id}/favorite?is_favorite=false",
            method="PATCH",
            token=api_token,
        )
        assert status == 200
        assert isinstance(body, dict)
        assert body.get("is_favorite") is False
    finally:
        delete_contact(app_url, api_token, contact_id)
