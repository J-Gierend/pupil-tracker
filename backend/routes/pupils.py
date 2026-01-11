"""Routes for pupils management."""
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Pupil

router = APIRouter()


class PupilCreate(BaseModel):
    """Schema for creating a pupil."""
    first_name: str
    last_name: str
    class_id: int


class PupilResponse(BaseModel):
    """Schema for pupil response."""
    id: int
    first_name: str
    last_name: str
    class_id: int

    class Config:
        from_attributes = True


@router.post("", response_model=PupilResponse, status_code=status.HTTP_201_CREATED)
def create_pupil(data: PupilCreate, db: Session = Depends(get_db)):
    """Create a new pupil."""
    pupil = Pupil(**data.model_dump())
    db.add(pupil)
    db.commit()
    db.refresh(pupil)
    return pupil


@router.get("", response_model=List[PupilResponse])
def get_pupils(class_id: Optional[int] = None, db: Session = Depends(get_db)):
    """Get all pupils, optionally filtered by class."""
    query = db.query(Pupil)
    if class_id:
        query = query.filter(Pupil.class_id == class_id)
    return query.all()


@router.get("/{pupil_id}", response_model=PupilResponse)
def get_pupil(pupil_id: int, db: Session = Depends(get_db)):
    """Get a pupil by ID."""
    pupil = db.query(Pupil).filter(Pupil.id == pupil_id).first()
    if not pupil:
        raise HTTPException(status_code=404, detail="Pupil not found")
    return pupil


@router.put("/{pupil_id}", response_model=PupilResponse)
def update_pupil(pupil_id: int, data: PupilCreate, db: Session = Depends(get_db)):
    """Update a pupil."""
    pupil = db.query(Pupil).filter(Pupil.id == pupil_id).first()
    if not pupil:
        raise HTTPException(status_code=404, detail="Pupil not found")
    for key, value in data.model_dump().items():
        setattr(pupil, key, value)
    db.commit()
    db.refresh(pupil)
    return pupil


@router.delete("/{pupil_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pupil(pupil_id: int, db: Session = Depends(get_db)):
    """Delete a pupil."""
    pupil = db.query(Pupil).filter(Pupil.id == pupil_id).first()
    if not pupil:
        raise HTTPException(status_code=404, detail="Pupil not found")
    db.delete(pupil)
    db.commit()
    return None
