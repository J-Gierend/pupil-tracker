"""Routes for entries management."""
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Entry

router = APIRouter()


class EntryCreate(BaseModel):
    """Schema for creating an entry."""
    pupil_id: int
    category_id: int
    date: date
    text: str
    grade: Optional[str] = None
    subject: Optional[str] = None


class EntryResponse(BaseModel):
    """Schema for entry response."""
    id: int
    pupil_id: int
    category_id: int
    date: date
    text: str
    grade: Optional[str]
    subject: Optional[str]

    class Config:
        from_attributes = True


@router.post("", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
def create_entry(data: EntryCreate, db: Session = Depends(get_db)):
    """Create a new entry."""
    entry = Entry(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("", response_model=List[EntryResponse])
def get_entries(
    pupil_id: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all entries, optionally filtered by pupil or category."""
    query = db.query(Entry)
    if pupil_id:
        query = query.filter(Entry.pupil_id == pupil_id)
    if category_id:
        query = query.filter(Entry.category_id == category_id)
    return query.all()


@router.get("/{entry_id}", response_model=EntryResponse)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    """Get an entry by ID."""
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.put("/{entry_id}", response_model=EntryResponse)
def update_entry(entry_id: int, data: EntryCreate, db: Session = Depends(get_db)):
    """Update an entry."""
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for key, value in data.model_dump().items():
        setattr(entry, key, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    """Delete an entry."""
    entry = db.query(Entry).filter(Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    return None
