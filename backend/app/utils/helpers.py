"""Utility functions"""

from datetime import datetime, timedelta


def generate_order_number() -> str:
    """Generate a unique order number"""
    from time import time
    return f"ORD-{int(time())}"


def calculate_discount(original_price: float, discount_percentage: float) -> float:
    """Calculate discount amount"""
    return original_price * (discount_percentage / 100)


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency"""
    if currency == "USD":
        return f"${amount:.2f}"
    elif currency == "EUR":
        return f"€{amount:.2f}"
    return f"{amount:.2f} {currency}"


def is_valid_phone(phone: str) -> bool:
    """Validate phone number format"""
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None


def paginate(total: int, page: int, page_size: int) -> dict:
    """Calculate pagination metadata"""
    total_pages = (total + page_size - 1) // page_size
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
