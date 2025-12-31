"""Database models for coupons"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.infrastructure.database.database import Base


class CouponStatusEnum(str, enum.Enum):
    """Coupon status enum"""
    ACTIVE = "active"
    EXPIRED = "expired"
    DISABLED = "disabled"


class Coupon(Base):
    """Coupon model"""
    __tablename__ = "coupons"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount_percentage = Column(Numeric(5, 2), nullable=True)
    discount_amount = Column(Numeric(10, 2), nullable=True)
    max_uses = Column(Integer, nullable=True)
    current_uses = Column(Integer, default=0, nullable=False)
    min_purchase_amount = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Coupon(id={self.id}, code={self.code})>"
