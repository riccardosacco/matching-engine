import uuid


def v4():
    """
    Generate UUIDv4
    Typical usage:
        >>> import generate_uuid
        >>> generate_uuid.v4()
    - Params: None
    - Return: UUID
    """
    return uuid.uuid4()
