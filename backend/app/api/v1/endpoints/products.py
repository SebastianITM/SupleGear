"""Product endpoints"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

from app.infrastructure.database.database import get_db
from app.application.products.create_product import (
    CreateProductUseCase, GetProductUseCase, UpdateProductUseCase,
    ListProductsUseCase, SearchProductsUseCase
)
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductResponse
from app.api.v1.dependencies import get_current_vendor

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_vendor)
):
    """Create a new product (vendor/admin only)"""
    try:
        use_case = CreateProductUseCase(db)
        return use_case.execute(product)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get product by ID"""
    try:
        use_case = GetProductUseCase(db)
        return use_case.execute(product_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_vendor)
):
    """Update product (vendor/admin only)"""
    try:
        use_case = UpdateProductUseCase(db)
        return use_case.execute(product_id, product_update)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/", response_model=list[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all active products"""
    use_case = ListProductsUseCase(db)
    return use_case.execute(skip, limit)


@router.get("/search/results", response_model=list[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search products"""
    use_case = SearchProductsUseCase(db)
    return use_case.execute(q, skip, limit)
