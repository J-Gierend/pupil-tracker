"""Routes for generating pupil reports."""
from datetime import date
from typing import Optional, Dict, Any, List
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Pupil, Entry
from services.pdf_generator import generate_pdf_report
from services.word_generator import generate_word_report

router = APIRouter()


class EntryData(BaseModel):
    """Schema for entry in report."""
    date: str
    text: str
    grade: Optional[str]
    subject: Optional[str]


class ReportResponse(BaseModel):
    """Schema for report response."""
    pupil_id: int
    pupil_name: str
    class_name: str
    start_date: str
    end_date: str
    entries_by_category: Dict[str, List[EntryData]]


def build_report_data(pupil: Pupil, entries: list, start: date, end: date) -> dict:
    """Build report data dictionary from pupil and entries."""
    entries_by_cat = defaultdict(list)
    for entry in entries:
        cat_name = entry.category.name_en
        entries_by_cat[cat_name].append({
            "date": str(entry.date),
            "text": entry.text,
            "grade": entry.grade,
            "subject": entry.subject
        })
    return {
        "pupil_id": pupil.id,
        "pupil_name": f"{pupil.first_name} {pupil.last_name}",
        "class_name": pupil.class_.name if pupil.class_ else "N/A",
        "start_date": str(start),
        "end_date": str(end),
        "entries_by_category": dict(entries_by_cat)
    }


DEFAULT_START_DATE = date(2000, 1, 1)
DEFAULT_END_DATE = date(2100, 12, 31)


def get_pupil_or_404(db: Session, pupil_id: int) -> Pupil:
    """Get pupil by ID or raise 404."""
    pupil = db.query(Pupil).filter(Pupil.id == pupil_id).first()
    if not pupil:
        raise HTTPException(status_code=404, detail="Pupil not found")
    return pupil


def get_pupil_report_data(
    db: Session,
    pupil_id: int,
    start_date: Optional[date],
    end_date: Optional[date]
) -> tuple:
    """Get pupil, entries, and build report data."""
    pupil = get_pupil_or_404(db, pupil_id)
    start = start_date or DEFAULT_START_DATE
    end = end_date or DEFAULT_END_DATE
    entries = db.query(Entry).filter(
        Entry.pupil_id == pupil_id,
        Entry.date >= start,
        Entry.date <= end
    ).all()
    report_data = build_report_data(pupil, entries, start, end)
    return pupil, report_data


@router.get("/pupil/{pupil_id}", response_model=ReportResponse)
def get_pupil_report(
    pupil_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get report data for a pupil."""
    _, report_data = get_pupil_report_data(db, pupil_id, start_date, end_date)
    return report_data


@router.get("/pupil/{pupil_id}/pdf")
def download_pdf_report(
    pupil_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Download PDF report for a pupil."""
    pupil, report_data = get_pupil_report_data(db, pupil_id, start_date, end_date)
    pdf_buffer = generate_pdf_report(report_data)
    filename = f"report_{pupil.last_name}_{pupil.first_name}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)


@router.get("/pupil/{pupil_id}/docx")
def download_word_report(
    pupil_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Download Word document report for a pupil."""
    pupil, report_data = get_pupil_report_data(db, pupil_id, start_date, end_date)
    docx_buffer = generate_word_report(report_data)
    filename = f"report_{pupil.last_name}_{pupil.first_name}.docx"
    media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(docx_buffer, media_type=media, headers=headers)
