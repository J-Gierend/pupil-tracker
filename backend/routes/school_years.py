"""Routes for school years management."""
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import SchoolYear

router = APIRouter()


class SchoolYearCreate(BaseModel):
    """Schema for creating a school year."""
    name: str
    start_date: date
    end_date: date
    is_active: bool = False


class SchoolYearResponse(BaseModel):
    """Schema for school year response."""
    id: int
    name: str
    start_date: date
    end_date: date
    is_active: bool

    class Config:
        from_attributes = True


@router.post("", response_model=SchoolYearResponse, status_code=status.HTTP_201_CREATED)
def create_school_year(data: SchoolYearCreate, db: Session = Depends(get_db)):
    """Create a new school year."""
    school_year = SchoolYear(**data.model_dump())
    db.add(school_year)
    db.commit()
    db.refresh(school_year)
    return school_year


@router.get("", response_model=List[SchoolYearResponse])
def get_school_years(db: Session = Depends(get_db)):
    """Get all school years."""
    return db.query(SchoolYear).all()


@router.get("/active", response_model=SchoolYearResponse)
def get_active_school_year(db: Session = Depends(get_db)):
    """Get the active school year."""
    school_year = db.query(SchoolYear).filter(SchoolYear.is_active == True).first()
    if not school_year:
        raise HTTPException(status_code=404, detail="No active school year")
    return school_year


@router.get("/{year_id}", response_model=SchoolYearResponse)
def get_school_year(year_id: int, db: Session = Depends(get_db)):
    """Get a school year by ID."""
    school_year = db.query(SchoolYear).filter(SchoolYear.id == year_id).first()
    if not school_year:
        raise HTTPException(status_code=404, detail="School year not found")
    return school_year


@router.put("/{year_id}", response_model=SchoolYearResponse)
def update_school_year(year_id: int, data: SchoolYearCreate, db: Session = Depends(get_db)):
    """Update a school year."""
    school_year = db.query(SchoolYear).filter(SchoolYear.id == year_id).first()
    if not school_year:
        raise HTTPException(status_code=404, detail="School year not found")
    for key, value in data.model_dump().items():
        setattr(school_year, key, value)
    db.commit()
    db.refresh(school_year)
    return school_year


@router.delete("/{year_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_year(year_id: int, db: Session = Depends(get_db)):
    """Delete a school year."""
    school_year = db.query(SchoolYear).filter(SchoolYear.id == year_id).first()
    if not school_year:
        raise HTTPException(status_code=404, detail="School year not found")
    db.delete(school_year)
    db.commit()
    return None
