"""Tests for reports API endpoints."""
from datetime import date, timedelta


def create_full_test_data(client):
    """Helper to create full test data with entries."""
    year_data = {
        "name": "2024/2025",
        "start_date": "2024-09-01",
        "end_date": "2025-07-31",
        "is_active": True
    }
    year_resp = client.post("/school_years", json=year_data)
    year_id = year_resp.json()["id"]

    class_resp = client.post("/classes", json={"name": "1A", "school_year_id": year_id})
    class_id = class_resp.json()["id"]

    pupil_resp = client.post("/pupils", json={
        "first_name": "Max", "last_name": "Mustermann", "class_id": class_id
    })
    pupil_id = pupil_resp.json()["id"]

    cat_resp = client.post("/categories", json={
        "name_de": "Test", "name_en": "Test", "is_predefined": False
    })
    cat_id = cat_resp.json()["id"]

    today = str(date.today())
    client.post("/entries", json={
        "pupil_id": pupil_id,
        "category_id": cat_id,
        "date": today,
        "text": "Test entry",
        "grade": "A",
        "subject": "Math"
    })

    return pupil_id


def test_get_pupil_report(client):
    """Test getting report data for a pupil."""
    pupil_id = create_full_test_data(client)
    response = client.get(f"/reports/pupil/{pupil_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["pupil_name"] == "Max Mustermann"
    assert "entries_by_category" in data


def test_get_pupil_report_with_date_range(client):
    """Test getting report with date filter."""
    pupil_id = create_full_test_data(client)
    today = date.today()
    start = str(today - timedelta(days=7))
    end = str(today + timedelta(days=1))

    response = client.get(f"/reports/pupil/{pupil_id}?start_date={start}&end_date={end}")
    assert response.status_code == 200


def test_get_pupil_report_not_found(client):
    """Test report for non-existent pupil."""
    response = client.get("/reports/pupil/999")
    assert response.status_code == 404


def test_download_pdf_report(client):
    """Test downloading PDF report."""
    pupil_id = create_full_test_data(client)
    response = client.get(f"/reports/pupil/{pupil_id}/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"


def test_download_word_report(client):
    """Test downloading Word document report."""
    pupil_id = create_full_test_data(client)
    response = client.get(f"/reports/pupil/{pupil_id}/docx")
    assert response.status_code == 200
    content_type = response.headers["content-type"]
    assert "application/vnd.openxmlformats" in content_type


def test_pdf_report_not_found(client):
    """Test PDF report for non-existent pupil."""
    response = client.get("/reports/pupil/999/pdf")
    assert response.status_code == 404


def test_word_report_not_found(client):
    """Test Word report for non-existent pupil."""
    response = client.get("/reports/pupil/999/docx")
    assert response.status_code == 404
