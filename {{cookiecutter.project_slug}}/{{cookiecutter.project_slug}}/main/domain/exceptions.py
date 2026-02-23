"""Domain exceptions."""


class DomainException(Exception):
    """Base domain exception."""


class ItemNotFoundException(DomainException):
    """Raised when an item is not found."""

    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Item not found: {item_id}")
