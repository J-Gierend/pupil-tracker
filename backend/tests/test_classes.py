"""Tests for classes API endpoints."""


def test_create_class(client, sample_school_year, sample_class):
    """Test creating a new class."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    response = client.post("/classes", json=class_data)
    assert response.status_code == 201
    assert response.json()["name"] == sample_class["name"]


def test_get_classes(client, sample_school_year, sample_class):
    """Test getting list of classes."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    client.post("/classes", json=class_data)

    response = client.get("/classes")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_class_by_id(client, sample_school_year, sample_class):
    """Test getting a class by ID."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    create_resp = client.post("/classes", json=class_data)
    class_id = create_resp.json()["id"]

    response = client.get(f"/classes/{class_id}")
    assert response.status_code == 200
    assert response.json()["name"] == sample_class["name"]


def test_get_class_not_found(client):
    """Test getting non-existent class."""
    response = client.get("/classes/999")
    assert response.status_code == 404


def test_update_class(client, sample_school_year, sample_class):
    """Test updating a class."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    create_resp = client.post("/classes", json=class_data)
    class_id = create_resp.json()["id"]

    updated = {"name": "Class 2B", "school_year_id": year_id}
    response = client.put(f"/classes/{class_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["name"] == "Class 2B"


def test_delete_class(client, sample_school_year, sample_class):
    """Test deleting a class."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    create_resp = client.post("/classes", json=class_data)
    class_id = create_resp.json()["id"]

    response = client.delete(f"/classes/{class_id}")
    assert response.status_code == 204


def test_get_classes_by_school_year(client, sample_school_year, sample_class):
    """Test getting classes filtered by school year."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    client.post("/classes", json=class_data)

    response = client.get(f"/classes?school_year_id={year_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
