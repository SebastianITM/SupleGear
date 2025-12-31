"""Product use cases"""

from sqlalchemy.orm import Session

from app.infrastructure.repositories.product_repository import ProductRepository, CategoryRepository
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductResponse


class CreateProductUseCase:
    """Use case for creating a new product"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)
    
    def execute(self, product_data: ProductCreate) -> ProductResponse:
        """Create a new product"""
        # Verify category exists
        category = self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise ValueError(f"Category with ID {product_data.category_id} not found")
        
        # Check if SKU already exists
        existing_product = self.repository.get_by_sku(product_data.sku)
        if existing_product:
            raise ValueError(f"Product with SKU {product_data.sku} already exists")
        
        # Create product
        product = self.repository.create(product_data)
        return ProductResponse.from_orm(product)


class GetProductUseCase:
    """Use case for retrieving a product"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def execute(self, product_id: int) -> ProductResponse:
        """Get product by ID"""
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        return ProductResponse.from_orm(product)


class UpdateProductUseCase:
    """Use case for updating a product"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)
    
    def execute(self, product_id: int, product_data: ProductUpdate) -> ProductResponse:
        """Update product"""
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # If category is being updated, verify it exists
        if product_data.category_id:
            category = self.category_repository.get_by_id(product_data.category_id)
            if not category:
                raise ValueError(f"Category with ID {product_data.category_id} not found")
        
        # If SKU is being updated, check for duplicates
        if product_data.sku and product_data.sku != product.sku:
            existing_product = self.repository.get_by_sku(product_data.sku)
            if existing_product:
                raise ValueError(f"Product with SKU {product_data.sku} already exists")
        
        # Update product
        updated_product = self.repository.update(product_id, product_data)
        return ProductResponse.from_orm(updated_product)


class ListProductsUseCase:
    """Use case for listing products"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def execute(self, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Get all active products"""
        products = self.repository.get_active_products(skip, limit)
        return [ProductResponse.from_orm(product) for product in products]


class SearchProductsUseCase:
    """Use case for searching products"""
    
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def execute(self, query: str, skip: int = 0, limit: int = 100) -> list[ProductResponse]:
        """Search products"""
        products = self.repository.search(query, skip, limit)
        return [ProductResponse.from_orm(product) for product in products]
