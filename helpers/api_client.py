import json
from urllib import error, parse, request

from config.settings import TEST_DATA


def api_request(
    base_url,
    path,
    method="GET",
    token=None,
    json_body=None,
    form_body=None,
):
    url = f"{base_url.rstrip('/')}{path}"
    headers = {"Accept": "application/json", "User-Agent": "qa-tests"}
    body = None

    if json_body is not None:
        headers["Content-Type"] = "application/json"
        body = json.dumps(json_body).encode("utf-8")
    elif form_body is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        body = parse.urlencode(form_body).encode("utf-8")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = request.Request(url, data=body, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=30) as resp:
            return resp.status, _read_json(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        return exc.code, _read_json(exc.read().decode("utf-8"))


def get_auth_token(base_url):
    user = TEST_DATA["known_user"]
    status, body = api_request(
        base_url,
        "/api/auth/login",
        method="POST",
        form_body={"username": user["email"], "password": user["password"]},
    )
    assert status == 200
    assert isinstance(body, dict) and body.get("access_token")
    return body["access_token"]


def create_contact(base_url, token, name):
    status, body = api_request(
        base_url,
        "/api/contacts",
        method="POST",
        token=token,
        json_body={
            "name": name,
            "phone_number": "5551234567",
            "country_code": "+1",
            "group_category": "work",
        },
    )
    assert status == 201
    assert isinstance(body, dict) and isinstance(body.get("id"), int)
    return body["id"]


def delete_contact(base_url, token, contact_id):
    status, _ = api_request(
        base_url,
        f"/api/contacts/{contact_id}",
        method="DELETE",
        token=token,
    )
    assert status == 204


def _read_json(text):
    text = text.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None
