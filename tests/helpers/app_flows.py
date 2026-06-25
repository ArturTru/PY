import uuid

def unique_email(prefix: str = "autotest") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}@example.com"

def unique_contact_name(prefix: str) -> str:
    return f"{prefix} {uuid.uuid4().hex[:6]}"
