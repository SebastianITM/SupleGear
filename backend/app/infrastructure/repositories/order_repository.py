"""Order repository"""

from sqlalchemy.orm import Session

from app.infrastructure.repositories.base_repository import BaseRepository
from app.infrastructure.database.models_order import Order, OrderItem, Payment


class OrderRepository(BaseRepository[Order, dict, dict]):
    """Order repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(db, Order)
    
    def get_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get orders by user"""
        return self.db.query(self.model).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_order_number(self, order_number: str) -> Order | None:
        """Get order by order number"""
        return self.db.query(self.model).filter(Order.order_number == order_number).first()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> list[Order]:
        """Get orders by status"""
        return self.db.query(self.model).filter(
            Order.status == status
        ).offset(skip).limit(limit).all()


class PaymentRepository(BaseRepository[Payment, dict, dict]):
    """Payment repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(db, Payment)
    
    def get_by_order(self, order_id: int) -> Payment | None:
        """Get payment by order"""
        return self.db.query(self.model).filter(Payment.order_id == order_id).first()
    
    def get_by_transaction_id(self, transaction_id: str) -> Payment | None:
        """Get payment by transaction ID"""
        return self.db.query(self.model).filter(
            Payment.transaction_id == transaction_id
        ).first()
