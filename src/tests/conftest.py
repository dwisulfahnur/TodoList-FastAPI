import pytest
from databases import Database
from starlette.testclient import TestClient

from src.db import DATABASE_URL
from src.db import database
from src.main import app

test_database = Database(DATABASE_URL, force_rollback=True)


@pytest.fixture
def client():
    app.dependency_overrides[database] = test_database
    with TestClient(app) as client:
        yield client
        app.dependency_overrides = {}
