"""Tests for categories API endpoints."""


def test_create_category(client, sample_category):
    """Test creating a new category."""
    response = client.post("/categories", json=sample_category)
    assert response.status_code == 201
    data = response.json()
    assert data["name_de"] == sample_category["name_de"]
    assert data["name_en"] == sample_category["name_en"]


def test_get_categories(client, sample_category):
    """Test getting list of categories."""
    client.post("/categories", json=sample_category)
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_get_category_by_id(client, sample_category):
    """Test getting a category by ID."""
    create_resp = client.post("/categories", json=sample_category)
    cat_id = create_resp.json()["id"]

    response = client.get(f"/categories/{cat_id}")
    assert response.status_code == 200
    assert response.json()["name_de"] == sample_category["name_de"]


def test_get_category_not_found(client):
    """Test getting non-existent category."""
    response = client.get("/categories/999")
    assert response.status_code == 404


def test_update_category(client, sample_category):
    """Test updating a category."""
    create_resp = client.post("/categories", json=sample_category)
    cat_id = create_resp.json()["id"]

    updated = {**sample_category, "name_de": "Neue Kategorie"}
    response = client.put(f"/categories/{cat_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["name_de"] == "Neue Kategorie"


def test_delete_category(client, sample_category):
    """Test deleting a category."""
    create_resp = client.post("/categories", json=sample_category)
    cat_id = create_resp.json()["id"]

    response = client.delete(f"/categories/{cat_id}")
    assert response.status_code == 204

    get_resp = client.get(f"/categories/{cat_id}")
    assert get_resp.status_code == 404


def test_get_predefined_categories(client):
    """Test getting predefined categories only."""
    response = client.get("/categories?predefined_only=true")
    assert response.status_code == 200


def test_cannot_delete_predefined_category(client):
    """Test that predefined categories cannot be deleted."""
    predefined = {
        "name_de": "Vordefiniert",
        "name_en": "Predefined",
        "is_predefined": True
    }
    create_resp = client.post("/categories", json=predefined)
    cat_id = create_resp.json()["id"]

    response = client.delete(f"/categories/{cat_id}")
    assert response.status_code == 403
