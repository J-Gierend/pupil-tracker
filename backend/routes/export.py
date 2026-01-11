"""Routes for data export and import."""
import csv
from datetime import date, datetime
from io import StringIO
from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import SchoolYear, Class, Pupil, Category, Entry


def parse_date(date_str: str) -> date:
    """Parse date string to date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()

router = APIRouter()


class SchoolYearImport(BaseModel):
    """Schema for school year import."""
    id: Optional[int] = None
    name: str
    start_date: str
    end_date: str
    is_active: bool = False


class ClassImport(BaseModel):
    """Schema for class import."""
    name: str
    school_year_id: int


class PupilImport(BaseModel):
    """Schema for pupil import."""
    first_name: str
    last_name: str
    class_id: int


class CategoryImport(BaseModel):
    """Schema for category import."""
    name_de: str
    name_en: str
    is_predefined: bool = False


class EntryImport(BaseModel):
    """Schema for entry import."""
    pupil_id: int
    category_id: int
    date: str
    text: str
    grade: Optional[str] = None
    subject: Optional[str] = None


class ImportData(BaseModel):
    """Schema for full import data."""
    school_years: List[SchoolYearImport] = []
    classes: List[ClassImport] = []
    pupils: List[PupilImport] = []
    categories: List[CategoryImport] = []
    entries: List[EntryImport] = []


@router.get("/export/json")
def export_json(db: Session = Depends(get_db)):
    """Export all data as JSON."""
    return {
        "school_years": [serialize_school_year(sy) for sy in db.query(SchoolYear).all()],
        "classes": [serialize_class(c) for c in db.query(Class).all()],
        "pupils": [serialize_pupil(p) for p in db.query(Pupil).all()],
        "categories": [serialize_category(c) for c in db.query(Category).all()],
        "entries": [serialize_entry(e) for e in db.query(Entry).all()]
    }


def serialize_school_year(sy):
    """Serialize school year to dict."""
    return {"id": sy.id, "name": sy.name, "start_date": str(sy.start_date),
            "end_date": str(sy.end_date), "is_active": sy.is_active}


def serialize_class(c):
    """Serialize class to dict."""
    return {"id": c.id, "name": c.name, "school_year_id": c.school_year_id}


def serialize_pupil(p):
    """Serialize pupil to dict."""
    return {"id": p.id, "first_name": p.first_name,
            "last_name": p.last_name, "class_id": p.class_id}


def serialize_category(c):
    """Serialize category to dict."""
    return {"id": c.id, "name_de": c.name_de,
            "name_en": c.name_en, "is_predefined": c.is_predefined}


def serialize_entry(e):
    """Serialize entry to dict."""
    return {"id": e.id, "pupil_id": e.pupil_id, "category_id": e.category_id,
            "date": str(e.date), "text": e.text, "grade": e.grade, "subject": e.subject}


@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    """Export all entries as CSV."""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Pupil", "Category", "Date", "Text", "Grade", "Subject"])

    for entry in db.query(Entry).all():
        pupil = entry.pupil
        pupil_name = f"{pupil.first_name} {pupil.last_name}" if pupil else "N/A"
        cat_name = entry.category.name_en if entry.category else "N/A"
        writer.writerow([pupil_name, cat_name, entry.date, entry.text,
                        entry.grade or "", entry.subject or ""])

    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=export.csv"}
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers=headers)


@router.post("/import/json")
def import_json(data: ImportData, db: Session = Depends(get_db)):
    """Import data from JSON."""
    id_mapping = {"school_years": {}, "classes": {}, "pupils": {}, "categories": {}}
    counts = {"school_years": 0, "classes": 0, "pupils": 0, "categories": 0, "entries": 0}

    # Import school years
    for sy in data.school_years:
        old_id = sy.id
        new_sy = SchoolYear(
            name=sy.name,
            start_date=parse_date(sy.start_date),
            end_date=parse_date(sy.end_date),
            is_active=sy.is_active
        )
        db.add(new_sy)
        db.flush()
        if old_id:
            id_mapping["school_years"][old_id] = new_sy.id
        counts["school_years"] += 1

    # Import classes with mapped school year IDs
    for c in data.classes:
        sy_id = id_mapping["school_years"].get(c.school_year_id, c.school_year_id)
        new_class = Class(name=c.name, school_year_id=sy_id)
        db.add(new_class)
        counts["classes"] += 1

    db.commit()
    return {"message": "Import successful", "imported": counts}
