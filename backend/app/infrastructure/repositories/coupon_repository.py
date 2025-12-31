"""Coupon repository"""

from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.repositories.base_repository import BaseRepository
from app.infrastructure.database.models_coupon import Coupon


class CouponRepository(BaseRepository[Coupon, dict, dict]):
    """Coupon repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(db, Coupon)
    
    def get_by_code(self, code: str) -> Coupon | None:
        """Get coupon by code"""
        return self.db.query(self.model).filter(Coupon.code == code).first()
    
    def get_active_coupons(self, skip: int = 0, limit: int = 100) -> list[Coupon]:
        """Get active and valid coupons"""
        now = datetime.utcnow()
        return self.db.query(self.model).filter(
            Coupon.is_active == True,
            Coupon.valid_from <= now,
            Coupon.valid_until >= now
        ).offset(skip).limit(limit).all()
    
    def validate_coupon(self, code: str) -> bool:
        """Validate if coupon can be used"""
        coupon = self.get_by_code(code)
        if not coupon:
            return False
        
        now = datetime.utcnow()
        if not coupon.is_active:
            return False
        if coupon.valid_from > now or coupon.valid_until < now:
            return False
        if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
            return False
        
        return True
