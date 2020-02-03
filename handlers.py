from datetime import datetime

import databases
from fastapi import APIRouter, HTTPException, Depends
from starlette import status

import crud
from db import get_database
from dbmodels import TodoItemInDB
from models import TodoItem, TodoItemIn

router = APIRouter()


@router.get('/todos', status_code=status.HTTP_200_OK, tags=["ToDo"])
async def get_todo_list_api(fields: str = None):
    database = get_database()
    if fields:
        fields = [c.strip() for c in fields.split(",")]
        fields = [getattr(TodoItemInDB.c, col, None) for col in fields if
                  getattr(TodoItemInDB.c, col, None) is not None]

    return await crud.select_todo(fields, database)


@router.post('/todos', response_model=TodoItem, status_code=status.HTTP_201_CREATED, tags=["ToDo"])
async def create_todo_api(todo: TodoItemIn, database: databases.Database = Depends(get_database)):
    return await crud.create_todo(todo.title, todo.description,database)


@router.get('/todos/{id}', status_code=status.HTTP_200_OK, tags=["ToDo"])
async def get_todo_detail_api(id: int, database: databases.Database = Depends(get_database), fields: str = ""):
    if fields:
        fields = [c.strip() for c in fields.split(",")]
        fields = [getattr(TodoItemInDB.c, col, None) for col in fields if
                  getattr(TodoItemInDB.c, col, None) is not None]

    todo = await crud.get_todo(id, fields, database)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")

    return todo


@router.delete('/todos/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["ToDo"])
async def delete_todo_api(id: int, database: databases.Database = Depends(get_database)):
    if not await crud.is_todo_exist(id, database):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item Not Found")

    await crud.delete_todo(id, database)
    return None
