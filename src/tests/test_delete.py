from starlette.testclient import TestClient

from src import crud


def test_delete_todo(client: TestClient, monkeypatch):
    async def mock_is_todo_exist(id, db):
        return True

    async def mock_delete_todo(id, db):
        return None

    monkeypatch.setattr(crud, "delete_todo", mock_delete_todo)
    monkeypatch.setattr(crud, "is_todo_exist", mock_is_todo_exist)

    r = client.delete("/api/v1/todos/1")
    assert r.status_code == 204
    assert r.text == "null"


def test_delete_todo_invalid_id(client: TestClient, monkeypatch):
    async def mock_is_todo_exist(id, db):
        return False

    monkeypatch.setattr(crud, "is_todo_exist", mock_is_todo_exist)
    r = client.delete("/api/v1/todos/1")
    assert r.status_code == 404
    assert r.json() == {"detail": "Item Not Found"}
