"""User use cases"""

from sqlalchemy.orm import Session

from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.core.security import hash_password, verify_password


class CreateUserUseCase:
    """Use case for creating a new user"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, user_data: UserCreate) -> UserResponse:
        """Create a new user"""
        # Check if user already exists
        existing_user = self.repository.get_by_email_or_username(
            user_data.email, user_data.username
        )
        if existing_user:
            raise ValueError("User with this email or username already exists")
        
        # Hash password
        user_dict = user_data.dict()
        user_dict["hashed_password"] = hash_password(user_dict.pop("password"))
        
        # Create user
        user = self.repository.create(UserCreate(**user_dict))
        return UserResponse.from_orm(user)


class GetUserUseCase:
    """Use case for retrieving a user"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, user_id: int) -> UserResponse:
        """Get user by ID"""
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return UserResponse.from_orm(user)


class UpdateUserUseCase:
    """Use case for updating a user"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        """Update user"""
        user = self.repository.update(user_id, user_data)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return UserResponse.from_orm(user)


class DeleteUserUseCase:
    """Use case for deleting a user"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, user_id: int) -> bool:
        """Delete user"""
        result = self.repository.delete(user_id)
        if not result:
            raise ValueError(f"User with ID {user_id} not found")
        return True


class SearchUsersUseCase:
    """Use case for searching users"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, query: str, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        """Search users"""
        users = self.repository.search(query, skip, limit)
        return [UserResponse.from_orm(user) for user in users]
