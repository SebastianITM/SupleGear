"""User repository"""

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.infrastructure.repositories.base_repository import BaseRepository
from app.infrastructure.database.models_user import User
from app.schemas.user_schemas import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """User repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(db, User)
    
    def get_by_email(self, email: str) -> User | None:
        """Get user by email"""
        return self.db.query(self.model).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> User | None:
        """Get user by username"""
        return self.db.query(self.model).filter(User.username == username).first()
    
    def get_by_email_or_username(self, email: str, username: str) -> User | None:
        """Get user by email or username"""
        return self.db.query(self.model).filter(
            or_(User.email == email, User.username == username)
        ).first()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[User]:
        """Search users by email or username"""
        return self.db.query(self.model).filter(
            or_(
                User.email.ilike(f"%{query}%"),
                User.username.ilike(f"%{query}%"),
                User.first_name.ilike(f"%{query}%"),
                User.last_name.ilike(f"%{query}%"),
            )
        ).offset(skip).limit(limit).all()
    
    def get_active_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get only active users"""
        return self.db.query(self.model).filter(User.is_active == True).offset(skip).limit(limit).all()
