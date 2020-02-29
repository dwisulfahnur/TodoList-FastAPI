from starlette.testclient import TestClient

from src import crud


def test_read_list_todos(client: TestClient):
    r = client.get("/api/v1/todos")
    assert r.status_code == 200
    assert type(r.json()) == list


def test_read_detail_todo(client: TestClient, monkeypatch):
    test_data = {
        "id": 1,
        "title": "Test fucking todo",
        "description": "description of fucking todo"
    }

    async def mock_get_todo(id, fields, db):
        return test_data

    monkeypatch.setattr(crud, "get_todo", mock_get_todo)

    r = client.get("/api/v1/todos/1")
    assert r.status_code == 200
    assert r.json() == test_data


def test_read_detail_invalid(client: TestClient, monkeypatch):
    async def mock_get_todo(id, fields, db):
        return None

    monkeypatch.setattr(crud, "get_todo", mock_get_todo)

    r = client.get("/api/v1/todos/1000")
    assert r.status_code == 404
    assert r.json()["detail"] == "Item Not Found"
