"""Test example for product creation"""

import pytest
from sqlalchemy.orm import Session

from app.application.products.create_product import CreateProductUseCase
from app.infrastructure.repositories.product_repository import ProductRepository, CategoryRepository
from app.schemas.product_schemas import ProductCreate


def test_create_product_success(db_session: Session):
    """Test successful product creation"""
    # First create a category
    category_repo = CategoryRepository(db_session)
    category_dict = {"name": "Proteins", "description": "Protein supplements"}
    category = category_repo.create(category_dict)
    
    # Create product
    product_data = ProductCreate(
        name="Whey Protein 5KG",
        description="High quality whey protein",
        price=99.99,
        stock=50,
        sku="WHEY-5KG-001",
        category_id=category.id
    )
    
    use_case = CreateProductUseCase(db_session)
    result = use_case.execute(product_data)
    
    assert result.id is not None
    assert result.name == "Whey Protein 5KG"
    assert result.sku == "WHEY-5KG-001"
    assert result.status == "active"


def test_create_product_duplicate_sku(db_session: Session):
    """Test that duplicate SKU raises error"""
    category_repo = CategoryRepository(db_session)
    category_dict = {"name": "Proteins", "description": "Protein supplements"}
    category = category_repo.create(category_dict)
    
    # Create first product
    product_repo = ProductRepository(db_session)
    product_dict = {
        "name": "Whey Protein",
        "price": 99.99,
        "stock": 50,
        "sku": "WHEY-001",
        "category_id": category.id
    }
    product_repo.create(product_dict)
    
    # Try to create second product with same SKU
    product_data = ProductCreate(
        name="Another Whey",
        price=99.99,
        stock=50,
        sku="WHEY-001",
        category_id=category.id
    )
    
    use_case = CreateProductUseCase(db_session)
    with pytest.raises(ValueError):
        use_case.execute(product_data)
