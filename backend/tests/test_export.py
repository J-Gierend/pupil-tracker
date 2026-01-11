"""Tests for export/import API endpoints."""
import json
from datetime import date


def create_full_test_data(client):
    """Helper to create full test data."""
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

    client.post("/entries", json={
        "pupil_id": pupil_id,
        "category_id": cat_id,
        "date": str(date.today()),
        "text": "Test entry",
        "grade": "A",
        "subject": "Math"
    })


def test_export_json(client):
    """Test exporting all data as JSON."""
    create_full_test_data(client)
    response = client.get("/export/json")
    assert response.status_code == 200
    data = response.json()
    assert "school_years" in data
    assert "classes" in data
    assert "pupils" in data
    assert "categories" in data
    assert "entries" in data


def test_export_csv(client):
    """Test exporting all data as CSV."""
    create_full_test_data(client)
    response = client.get("/export/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]


def test_import_json(client):
    """Test importing data from JSON."""
    import_data = {
        "school_years": [{
            "name": "2025/2026",
            "start_date": "2025-09-01",
            "end_date": "2026-07-31",
            "is_active": False
        }],
        "classes": [],
        "pupils": [],
        "categories": [],
        "entries": []
    }
    response = client.post("/import/json", json=import_data)
    assert response.status_code == 200
    assert response.json()["imported"]["school_years"] == 1


def test_import_json_with_classes(client):
    """Test importing data with relationships."""
    import_data = {
        "school_years": [{
            "id": 1,
            "name": "2025/2026",
            "start_date": "2025-09-01",
            "end_date": "2026-07-31",
            "is_active": False
        }],
        "classes": [{
            "name": "2A",
            "school_year_id": 1
        }],
        "pupils": [],
        "categories": [],
        "entries": []
    }
    response = client.post("/import/json", json=import_data)
    assert response.status_code == 200
    assert response.json()["imported"]["classes"] == 1


def test_export_empty_database(client):
    """Test exporting when database is empty."""
    response = client.get("/export/json")
    assert response.status_code == 200
    data = response.json()
    assert data["school_years"] == []
