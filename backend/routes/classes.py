"""Routes for classes management."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Class

router = APIRouter()


class ClassCreate(BaseModel):
    """Schema for creating a class."""
    name: str
    school_year_id: int


class ClassResponse(BaseModel):
    """Schema for class response."""
    id: int
    name: str
    school_year_id: int

    class Config:
        from_attributes = True


@router.post("", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(data: ClassCreate, db: Session = Depends(get_db)):
    """Create a new class."""
    class_ = Class(**data.model_dump())
    db.add(class_)
    db.commit()
    db.refresh(class_)
    return class_


@router.get("", response_model=List[ClassResponse])
def get_classes(school_year_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all classes, optionally filtered by school year."""
    query = db.query(Class)
    if school_year_id:
        query = query.filter(Class.school_year_id == school_year_id)
    return query.all()


@router.get("/{class_id}", response_model=ClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)):
    """Get a class by ID."""
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(class_id: int, data: ClassCreate, db: Session = Depends(get_db)):
    """Update a class."""
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    for key, value in data.model_dump().items():
        setattr(class_, key, value)
    db.commit()
    db.refresh(class_)
    return class_


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: int, db: Session = Depends(get_db)):
    """Delete a class."""
    class_ = db.query(Class).filter(Class.id == class_id).first()
    if not class_:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(class_)
    db.commit()
    return None
