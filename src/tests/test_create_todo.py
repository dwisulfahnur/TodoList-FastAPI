from datetime import datetime
import dateutil.parser
from starlette.testclient import TestClient


def test_create_todo(client: TestClient):
    data = {"title": "first test todo", "description": "description test todo"}

    r = client.post("/api/v1/todos", json=data)

    assert r.status_code == 201
    assert r.json()["title"] == data["title"]
    assert r.json()["description"] == data["description"]
    assert dateutil.parser.isoparse(r.json()["created_at"]) < datetime.now()
    assert dateutil.parser.isoparse(r.json()["updated_at"]) < datetime.now()



def test_create_todo_invalid_payload(client: TestClient):
    data = {"title": "", "description": "description test todo"}
    r = client.post("/api/v1/todos", json=data)
    assert r.status_code == 422
