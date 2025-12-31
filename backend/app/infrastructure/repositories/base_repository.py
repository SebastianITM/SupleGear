"""Base repository with common CRUD operations"""

from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

T = TypeVar("T")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[T, CreateSchemaType, UpdateSchemaType]):
    """Base repository with CRUD operations"""
    
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model
    
    def create(self, obj_in: CreateSchemaType) -> T:
        """Create a new object"""
        db_obj = self.model(**obj_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def get_by_id(self, obj_id: int) -> Optional[T]:
        """Get object by ID"""
        return self.db.query(self.model).filter(self.model.id == obj_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all objects with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, obj_id: int, obj_in: UpdateSchemaType) -> Optional[T]:
        """Update an object"""
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return None
        
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, obj_id: int) -> bool:
        """Delete an object"""
        db_obj = self.get_by_id(obj_id)
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def exists(self, obj_id: int) -> bool:
        """Check if object exists"""
        return self.db.query(self.model).filter(self.model.id == obj_id).first() is not None
