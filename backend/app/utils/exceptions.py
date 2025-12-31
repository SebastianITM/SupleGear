"""Custom exceptions"""


class SupleGearException(Exception):
    """Base exception for SupleGear"""
    pass


class ResourceNotFoundError(SupleGearException):
    """Raised when a resource is not found"""
    pass


class DuplicateResourceError(SupleGearException):
    """Raised when trying to create a duplicate resource"""
    pass


class InvalidCredentialsError(SupleGearException):
    """Raised when authentication fails"""
    pass


class InsufficientStockError(SupleGearException):
    """Raised when product stock is insufficient"""
    pass


class InvalidCouponError(SupleGearException):
    """Raised when coupon is invalid or expired"""
    pass


class PaymentFailedError(SupleGearException):
    """Raised when payment processing fails"""
    pass
