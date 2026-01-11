"""Tests for entries API endpoints."""
from datetime import date


def create_test_pupil_and_category(client, sample_school_year, sample_class, sample_pupil):
    """Helper to create prerequisite data."""
    year_resp = client.post("/school_years", json=sample_school_year)
    class_data = {**sample_class, "school_year_id": year_resp.json()["id"]}
    class_resp = client.post("/classes", json=class_data)
    pupil_data = {**sample_pupil, "class_id": class_resp.json()["id"]}
    pupil_resp = client.post("/pupils", json=pupil_data)

    category = {"name_de": "Test", "name_en": "Test", "is_predefined": False}
    cat_resp = client.post("/categories", json=category)

    return pupil_resp.json()["id"], cat_resp.json()["id"]


def test_create_entry(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test creating a new entry."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    response = client.post("/entries", json=entry_data)
    assert response.status_code == 201
    assert response.json()["text"] == sample_entry["text"]


def test_get_entries(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test getting list of entries."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    client.post("/entries", json=entry_data)

    response = client.get("/entries")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_entry_by_id(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test getting an entry by ID."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    create_resp = client.post("/entries", json=entry_data)
    entry_id = create_resp.json()["id"]

    response = client.get(f"/entries/{entry_id}")
    assert response.status_code == 200
    assert response.json()["text"] == sample_entry["text"]


def test_get_entry_not_found(client):
    """Test getting non-existent entry."""
    response = client.get("/entries/999")
    assert response.status_code == 404


def test_update_entry(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test updating an entry."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    create_resp = client.post("/entries", json=entry_data)
    entry_id = create_resp.json()["id"]

    updated = {**entry_data, "text": "Updated text"}
    response = client.put(f"/entries/{entry_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["text"] == "Updated text"


def test_delete_entry(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test deleting an entry."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    create_resp = client.post("/entries", json=entry_data)
    entry_id = create_resp.json()["id"]

    response = client.delete(f"/entries/{entry_id}")
    assert response.status_code == 204


def test_get_entries_by_pupil(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test getting entries filtered by pupil."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    client.post("/entries", json=entry_data)

    response = client.get(f"/entries?pupil_id={pupil_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_entries_by_category(client, sample_school_year, sample_class, sample_pupil, sample_entry):
    """Test getting entries filtered by category."""
    pupil_id, cat_id = create_test_pupil_and_category(
        client, sample_school_year, sample_class, sample_pupil
    )
    entry_data = {**sample_entry, "pupil_id": pupil_id, "category_id": cat_id}
    client.post("/entries", json=entry_data)

    response = client.get(f"/entries?category_id={cat_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
