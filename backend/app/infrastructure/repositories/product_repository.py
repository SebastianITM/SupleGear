"""Product repository"""

from sqlalchemy.orm import Session

from app.infrastructure.repositories.base_repository import BaseRepository
from app.infrastructure.database.models_product import Product, Category
from app.schemas.product_schemas import ProductCreate, ProductUpdate


class ProductRepository(BaseRepository[Product, ProductCreate, ProductUpdate]):
    """Product repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(db, Product)
    
    def get_by_sku(self, sku: str) -> Product | None:
        """Get product by SKU"""
        return self.db.query(self.model).filter(Product.sku == sku).first()
    
    def get_by_category(self, category_id: int, skip: int = 0, limit: int = 100) -> list[Product]:
        """Get products by category"""
        return self.db.query(self.model).filter(
            Product.category_id == category_id
        ).offset(skip).limit(limit).all()
    
    def search(self, query: str, skip: int = 0, limit: int = 100) -> list[Product]:
        """Search products by name or description"""
        return self.db.query(self.model).filter(
            Product.name.ilike(f"%{query}%") | Product.description.ilike(f"%{query}%")
        ).offset(skip).limit(limit).all()
    
    def get_active_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """Get only active products"""
        return self.db.query(self.model).filter(
            Product.status == "active"
        ).offset(skip).limit(limit).all()
    
    def get_low_stock(self, threshold: int = 10) -> list[Product]:
        """Get products with low stock"""
        return self.db.query(self.model).filter(
            Product.stock <= threshold,
            Product.status == "active"
        ).all()


class CategoryRepository(BaseRepository[Category, dict, dict]):
    """Category repository with custom queries"""
    
    def __init__(self, db: Session):
        super().__init__(db, Category)
    
    def get_by_name(self, name: str) -> Category | None:
        """Get category by name"""
        return self.db.query(self.model).filter(Category.name == name).first()
