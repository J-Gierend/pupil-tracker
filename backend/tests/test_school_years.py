"""Tests for school years API endpoints."""


def test_create_school_year(client, sample_school_year):
    """Test creating a new school year."""
    response = client.post("/school_years", json=sample_school_year)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_school_year["name"]
    assert data["is_active"] is True


def test_get_school_years(client, sample_school_year):
    """Test getting list of school years."""
    client.post("/school_years", json=sample_school_year)
    response = client.get("/school_years")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_get_school_year_by_id(client, sample_school_year):
    """Test getting a school year by ID."""
    create_resp = client.post("/school_years", json=sample_school_year)
    year_id = create_resp.json()["id"]

    response = client.get(f"/school_years/{year_id}")
    assert response.status_code == 200
    assert response.json()["name"] == sample_school_year["name"]


def test_get_school_year_not_found(client):
    """Test getting non-existent school year."""
    response = client.get("/school_years/999")
    assert response.status_code == 404


def test_update_school_year(client, sample_school_year):
    """Test updating a school year."""
    create_resp = client.post("/school_years", json=sample_school_year)
    year_id = create_resp.json()["id"]

    updated = {**sample_school_year, "name": "2025/2026"}
    response = client.put(f"/school_years/{year_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["name"] == "2025/2026"


def test_delete_school_year(client, sample_school_year):
    """Test deleting a school year."""
    create_resp = client.post("/school_years", json=sample_school_year)
    year_id = create_resp.json()["id"]

    response = client.delete(f"/school_years/{year_id}")
    assert response.status_code == 204

    get_resp = client.get(f"/school_years/{year_id}")
    assert get_resp.status_code == 404


def test_get_active_school_year(client, sample_school_year):
    """Test getting the active school year."""
    client.post("/school_years", json=sample_school_year)
    response = client.get("/school_years/active")
    assert response.status_code == 200
    assert response.json()["is_active"] is True
