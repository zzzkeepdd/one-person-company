import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_todos():
    from main import todos
    todos.clear()
    yield
    todos.clear()

def test_get_todos_empty():
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    response = client.post("/todos", json={"title": "测试任务"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试任务"
    assert data["completed"] is False

def test_create_todo_empty_body():
    response = client.post("/todos", json={})
    assert response.status_code == 422

def test_get_todo_by_id():
    create_resp = client.post("/todos", json={"title": "测试"})
    todo_id = create_resp.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "测试"

def test_get_todo_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404

def test_get_todo_invalid_id():
    response = client.get("/todos/invalid")
    assert response.status_code == 404

def test_update_todo():
    create_resp = client.post("/todos", json={"title": "原始"})
    todo_id = create_resp.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "更新", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新"
    assert data["completed"] is True

def test_update_todo_not_found():
    response = client.put("/todos/999", json={"title": "更新"})
    assert response.status_code == 404

def test_delete_todo():
    create_resp = client.post("/todos", json={"title": "待删除"})
    todo_id = create_resp.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    get_resp = client.get(f"/todos/{todo_id}")
    assert get_resp.status_code == 404

def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
