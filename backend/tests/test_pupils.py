"""Tests for pupils API endpoints."""


def test_create_pupil(client, sample_school_year, sample_class, sample_pupil):
    """Test creating a new pupil."""
    year_resp = client.post("/school_years", json=sample_school_year)
    year_id = year_resp.json()["id"]

    class_data = {**sample_class, "school_year_id": year_id}
    class_resp = client.post("/classes", json=class_data)
    class_id = class_resp.json()["id"]

    pupil_data = {**sample_pupil, "class_id": class_id}
    response = client.post("/pupils", json=pupil_data)
    assert response.status_code == 201
    assert response.json()["first_name"] == sample_pupil["first_name"]


def test_get_pupils(client, sample_school_year, sample_class, sample_pupil):
    """Test getting list of pupils."""
    year_resp = client.post("/school_years", json=sample_school_year)
    class_data = {**sample_class, "school_year_id": year_resp.json()["id"]}
    class_resp = client.post("/classes", json=class_data)
    pupil_data = {**sample_pupil, "class_id": class_resp.json()["id"]}
    client.post("/pupils", json=pupil_data)

    response = client.get("/pupils")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_pupil_by_id(client, sample_school_year, sample_class, sample_pupil):
    """Test getting a pupil by ID."""
    year_resp = client.post("/school_years", json=sample_school_year)
    class_data = {**sample_class, "school_year_id": year_resp.json()["id"]}
    class_resp = client.post("/classes", json=class_data)
    pupil_data = {**sample_pupil, "class_id": class_resp.json()["id"]}
    create_resp = client.post("/pupils", json=pupil_data)
    pupil_id = create_resp.json()["id"]

    response = client.get(f"/pupils/{pupil_id}")
    assert response.status_code == 200
    assert response.json()["first_name"] == sample_pupil["first_name"]


def test_get_pupil_not_found(client):
    """Test getting non-existent pupil."""
    response = client.get("/pupils/999")
    assert response.status_code == 404


def test_update_pupil(client, sample_school_year, sample_class, sample_pupil):
    """Test updating a pupil."""
    year_resp = client.post("/school_years", json=sample_school_year)
    class_data = {**sample_class, "school_year_id": year_resp.json()["id"]}
    class_resp = client.post("/classes", json=class_data)
    class_id = class_resp.json()["id"]
    pupil_data = {**sample_pupil, "class_id": class_id}
    create_resp = client.post("/pupils", json=pupil_data)
    pupil_id = create_resp.json()["id"]

    updated = {"first_name": "Anna", "last_name": "Schmidt", "class_id": class_id}
    response = client.put(f"/pupils/{pupil_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Anna"


def test_delete_pupil(client, sample_school_year, sample_class, sample_pupil):
    """Test deleting a pupil."""
    year_resp = client.post("/school_years", json=sample_school_year)
    class_data = {**sample_class, "school_year_id": year_resp.json()["id"]}
    class_resp = client.post("/classes", json=class_data)
    pupil_data = {**sample_pupil, "class_id": class_resp.json()["id"]}
    create_resp = client.post("/pupils", json=pupil_data)
    pupil_id = create_resp.json()["id"]

    response = client.delete(f"/pupils/{pupil_id}")
    assert response.status_code == 204


def test_get_pupils_by_class(client, sample_school_year, sample_class, sample_pupil):
    """Test getting pupils filtered by class."""
    year_resp = client.post("/school_years", json=sample_school_year)
    class_data = {**sample_class, "school_year_id": year_resp.json()["id"]}
    class_resp = client.post("/classes", json=class_data)
    class_id = class_resp.json()["id"]
    pupil_data = {**sample_pupil, "class_id": class_id}
    client.post("/pupils", json=pupil_data)

    response = client.get(f"/pupils?class_id={class_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
