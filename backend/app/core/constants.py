"""Application constants"""

# Role constants
class UserRole:
    """User role constants"""
    ADMIN = "admin"
    VENDOR = "vendor"
    CUSTOMER = "customer"
    
    ALL_ROLES = [ADMIN, VENDOR, CUSTOMER]


# Product constants
class ProductStatus:
    """Product status constants"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"
    
    ALL_STATUSES = [ACTIVE, INACTIVE, DISCONTINUED]


# Order constants
class OrderStatus:
    """Order status constants"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
    ALL_STATUSES = [PENDING, CONFIRMED, PROCESSING, SHIPPED, DELIVERED, CANCELLED]


class PaymentStatus:
    """Payment status constants"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    
    ALL_STATUSES = [PENDING, COMPLETED, FAILED, REFUNDED]


# Coupon constants
class CouponStatus:
    """Coupon status constants"""
    ACTIVE = "active"
    EXPIRED = "expired"
    DISABLED = "disabled"
    
    ALL_STATUSES = [ACTIVE, EXPIRED, DISABLED]


# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
DEFAULT_PAGE = 1

# Validation
PASSWORD_MIN_LENGTH = 8
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 50
EMAIL_MAX_LENGTH = 255

# Error messages
class ErrorMessages:
    """Standard error messages"""
    NOT_FOUND = "Resource not found"
    ALREADY_EXISTS = "Resource already exists"
    UNAUTHORIZED = "Unauthorized access"
    FORBIDDEN = "Access forbidden"
    INVALID_CREDENTIALS = "Invalid username or password"
    TOKEN_EXPIRED = "Token has expired"
    INVALID_TOKEN = "Invalid token"
    VALIDATION_ERROR = "Validation error"
    INTERNAL_ERROR = "Internal server error"
