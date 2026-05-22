from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI()

todos = []

class TodoCreate(BaseModel):
    model_config = {"extra": "forbid"}
    title: str = Field(..., min_length=1)
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    model_config = {"extra": "forbid"}
    title: Optional[str] = Field(None, min_length=1)
    completed: Optional[bool] = None

def get_todo_or_404(todo_id: str) -> dict:
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="任务不存在")

@app.get("/todos")
def get_todos():
    return todos

@app.get("/todos/{todo_id}")
def get_todo(todo_id: str):
    return get_todo_or_404(todo_id)

@app.post("/todos", status_code=201)
def create_todo(todo: TodoCreate):
    new_todo = {
        "id": str(uuid.uuid4()),
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    todos.append(new_todo)
    return new_todo

@app.put("/todos/{todo_id}")
def update_todo(todo_id: str, todo_update: TodoUpdate):
    todo = get_todo_or_404(todo_id)
    if todo_update.title is not None:
        todo["title"] = todo_update.title
    if todo_update.completed is not None:
        todo["completed"] = todo_update.completed
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    todo = get_todo_or_404(todo_id)
    todos.remove(todo)
    return {"message": "删除成功"}
