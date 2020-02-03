import pytest
from databases import Database
from sqlalchemy import create_engine
from starlette.testclient import TestClient

from db import get_database
from dbmodels import metadata
from main import app

DATABASE_URL = "mysql://root:root@127.0.0.1/test_todolistFastapi"
database = Database(DATABASE_URL, force_rollback=True)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
metadata.create_all(engine)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def get_database_test():
    return database


@pytest.fixture
def client():
    app.dependency_overrides[get_database] = get_database_test
    with TestClient(app) as client:
        yield client
        app.dependency_overrides = {}
