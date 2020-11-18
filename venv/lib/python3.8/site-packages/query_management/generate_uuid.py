import uuid


def v4():
    """
    Generate UUIDv4
    Usage:
        >>> from query_management import generate_uuid
        >>> generate_uuid.v4()
    - Params: None
    - Return: UUID
    """
    return uuid.uuid4()
