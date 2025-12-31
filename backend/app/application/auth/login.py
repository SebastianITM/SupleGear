"""Authentication use cases"""

from sqlalchemy.orm import Session

from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.auth_schemas import TokenRequest, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token


class LoginUseCase:
    """Use case for user login"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, credentials: TokenRequest) -> TokenResponse:
        """Authenticate user and generate tokens"""
        # Find user by email
        user = self.repository.get_by_email(credentials.email)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is inactive")
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id), "role": user.role})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )


class RefreshTokenUseCase:
    """Use case for refreshing access token"""
    
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def execute(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token"""
        from app.core.security import decode_token
        
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") == "refresh":
            raise ValueError("Invalid refresh token")
        
        user_id = payload.get("sub")
        user = self.repository.get_by_id(int(user_id))
        if not user:
            raise ValueError("User not found")
        
        # Generate new access token
        access_token = create_access_token({"sub": str(user.id), "role": user.role})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
