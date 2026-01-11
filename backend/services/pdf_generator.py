"""PDF report generator service."""
from io import BytesIO
from typing import Dict, Any

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def generate_pdf_report(report_data: Dict[str, Any]) -> BytesIO:
    """Generate a PDF report for a pupil."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16)
    title = f"Development Report: {report_data['pupil_name']}"
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.5*cm))

    # Period
    period = f"Period: {report_data['start_date']} - {report_data['end_date']}"
    story.append(Paragraph(period, styles['Normal']))
    story.append(Spacer(1, 0.5*cm))

    # Entries by category
    for category, entries in report_data.get('entries_by_category', {}).items():
        story.append(Paragraph(category, styles['Heading2']))
        for entry in entries:
            entry_text = f"[{entry['date']}] {entry['text']}"
            if entry.get('grade'):
                entry_text += f" (Grade: {entry['grade']})"
            story.append(Paragraph(entry_text, styles['Normal']))
        story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    buffer.seek(0)
    return buffer
