"""User endpoints"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.application.users.create_user import (
    CreateUserUseCase, GetUserUseCase, UpdateUserUseCase,
    DeleteUserUseCase, SearchUsersUseCase
)
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.api.v1.dependencies import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user"""
    try:
        use_case = CreateUserUseCase(db)
        return use_case.execute(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get user by ID"""
    try:
        use_case = GetUserUseCase(db)
        return use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update user"""
    try:
        use_case = UpdateUserUseCase(db)
        return use_case.execute(user_id, user_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    """Delete user (admin only)"""
    try:
        use_case = DeleteUserUseCase(db)
        use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/search/results", response_model=list[UserResponse])
async def search_users(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin)
):
    """Search users (admin only)"""
    try:
        use_case = SearchUsersUseCase(db)
        return use_case.execute(q, skip, limit)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
