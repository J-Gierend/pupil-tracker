"""Routes for categories management."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Category

router = APIRouter()


class CategoryCreate(BaseModel):
    """Schema for creating a category."""
    name_de: str
    name_en: str
    is_predefined: bool = False


class CategoryResponse(BaseModel):
    """Schema for category response."""
    id: int
    name_de: str
    name_en: str
    is_predefined: bool

    class Config:
        from_attributes = True


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    """Create a new category."""
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("", response_model=List[CategoryResponse])
def get_categories(predefined_only: bool = False, db: Session = Depends(get_db)):
    """Get all categories, optionally filtered to predefined only."""
    query = db.query(Category)
    if predefined_only:
        query = query.filter(Category.is_predefined == True)
    return query.all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    """Update a category."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in data.model_dump().items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Delete a category (predefined categories cannot be deleted)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if category.is_predefined:
        raise HTTPException(status_code=403, detail="Cannot delete predefined category")
    db.delete(category)
    db.commit()
    return None
