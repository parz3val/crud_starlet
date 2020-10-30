# Imports
from starlette.testclient import TestClient
from app import app


client = TestClient(app)


# Test the root/homepage url
def test_root_url():
    assert app.url_path_for("root") == "/"


# Test the URLs and routers
def test_url():
    assert app.url_path_for("all_notes") == "/all"

    assert app.url_path_for("create_note") == "/create"

    assert app.url_path_for("edit_note", note_id=4) == "/edit_note/4"

    assert app.url_path_for("delete_note", note_id=4) == "/delete_note/4"

    assert app.url_path_for("note_by_id", note_id=4) == "/note/4"


# Test all the routes and the access code
def test_routes():
    response = client.get("/")
    assert response.status_code == 200

    response = client.post("/")
    assert response.status_code == 405
    assert response.text.lower() == "method not allowed"

    response = client.get("/notes")
    assert response.status_code == 404
    assert response.text.lower() == "not found"

    response = client.get("/all")
    assert response.status_code == 200

    response = client.get("/create")
    assert response.status_code == 405
    assert response.text.lower() == "method not allowed"

    response = client.post("/create")
    assert response.status_code == 200
    assert response.text.lower() == "invalid or empty value"

    response = client.get("/edit_note")
    assert response.status_code == 404
    assert response.text.lower() == "not found"

    response = client.post("/edit_note")
    assert response.status_code == 404
    assert response.text.lower() == "not found"

    response = client.post("/edit_note/4")
    assert response.status_code == 200
    assert response.text.lower() == "invalid data or id"

    response = client.get("/delete_note")
    assert response.status_code == 404
    assert response.text.lower() == "not found"

    response = client.post("/delete_note")
    assert response.status_code == 404
    assert response.text.lower() == "not found"

    response = client.post("/delete_note/1")
    assert response.status_code == 200
    assert response.text.lower() == "delete 0"

    response = client.post("/note/")
    assert response.status_code == 404
    assert response.text.lower() == "not found"

    response = client.post("/note/1")
    assert response.status_code == 405
    assert response.text.lower() == "method not allowed"

    response = client.get("/note/2")
    assert response.status_code == 200


# Test JSON output from the endpoints
def test_view_endpoint():

    # Test singlee not view
    response = client.get("note/6/")
    assert response.json() == {
        "id": 6,
        "title": "This is final note",
        "content": "Okay things are working now. Which is nice",
        "date_created": "2020-10-30",
    }


# Test homepage JSON responsee
def test_root_view():
    response = client.get("/")
    assert response.json() == {"ms": "Welcome to Notes app."}


# Test creating note.
def test_create_note_endpoint():
    data = {"title": "Test note", "content": "Added from test client"}
    response = client.post("/create", json=data)

    assert response.status_code == 200
    assert response.text.lower() == "note created"


# Test /all endpoint for data
def test_all_notes():
    response = client.get("/all")
    assert response.json() is not None
