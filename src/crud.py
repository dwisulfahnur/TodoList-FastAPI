from datetime import datetime
from typing import List

from databases import Database
from sqlalchemy import select, desc

from src.db import get_database
from src.dbmodels import TodoItemInDB
from src.models import TodoItem


async def create_todo(
        title: str, description: str,
        db: Database = get_database()
) -> TodoItem:
    new_todo = dict(
        title=title,
        description=description,
        created_at=datetime.now(),
        updated_at=datetime.now())
    id = await db.execute(TodoItemInDB.insert(new_todo))

    return TodoItem(**dict(id=id, **new_todo))


async def get_todo(
        id: int, fields: List = [],
        db: Database = get_database()
):
    return await db.fetch_one(
        select(fields if fields else TodoItemInDB.columns)
            .where(TodoItemInDB.c.id == id)
            .limit(1))


async def select_todo(fields: List = [], db: Database = get_database()):
    return await db.fetch_all(select(fields if fields else TodoItemInDB.columns)
                              .select_from(TodoItemInDB)
                              .order_by(desc("created_at")))


async def is_todo_exist(id: int, db: Database = get_database()) -> bool:
    query = TodoItemInDB.count().where(TodoItemInDB.c.id == id)
    return True if await db.fetch_one(query) else False


async def delete_todo(id: int, db: Database = get_database()) -> None:
    await db.execute(TodoItemInDB.delete(TodoItemInDB.c.id == id))
    return None
