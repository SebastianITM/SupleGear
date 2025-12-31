"""Product schemas/DTOs"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal
from enum import Enum


class ProductStatus(str, Enum):
    """Product status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DISCONTINUED = "discontinued"


class ProductBase(BaseModel):
    """Base product schema"""
    name: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    sku: str = Field(..., min_length=3, max_length=50)
    category_id: int


class ProductCreate(ProductBase):
    """Product creation schema"""
    pass


class ProductUpdate(BaseModel):
    """Product update schema"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    sku: Optional[str] = Field(None, min_length=3, max_length=50)
    category_id: Optional[int] = None
    status: Optional[ProductStatus] = None


class ProductResponse(ProductBase):
    """Product response schema"""
    id: int
    status: ProductStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductDetailedResponse(ProductResponse):
    """Detailed product response"""
    images: list = []
    ratings_average: Optional[float] = None
    ratings_count: int = 0
