"""Authentication endpoints"""

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.application.auth.login import LoginUseCase, RefreshTokenUseCase
from app.schemas.auth_schemas import TokenRequest, TokenResponse, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: TokenRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint
    
    - **email**: User email
    - **password**: User password
    """
    try:
        use_case = LoginUseCase(db)
        return use_case.execute(credentials)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    try:
        use_case = RefreshTokenUseCase(db)
        return use_case.execute(request.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
