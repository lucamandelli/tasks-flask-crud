import requests

BASE_URL = "http://127.0.0.1:5000"


def test_get_tasks_empty():
    resp = requests.get(f"{BASE_URL}/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert "Tasks" in data
    assert data["Total tasks"] == 0


def test_create_task():
    payload = {"title": "Test Task", "description": "Test Desc"}
    resp = requests.post(f"{BASE_URL}/tasks", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["message"] == "Task created successfully"


def test_get_tasks_after_create():
    resp = requests.get(f"{BASE_URL}/tasks")
    assert resp.status_code == 200
    data = resp.json()
    assert data["Total tasks"] >= 1
    assert any(task["title"] == "Test Task" for task in data["Tasks"])


def test_get_task_by_id():
    resp = requests.get(f"{BASE_URL}/tasks/0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Test Task"


def test_patch_task_by_id():
    payload = {"title": "Updated Task", "completed": True}
    resp = requests.patch(f"{BASE_URL}/tasks/0", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Task updated successfully"

    resp2 = requests.get(f"{BASE_URL}/tasks/0")
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["title"] == "Updated Task"
    assert data2["completed"] is True


def test_delete_task_by_id():
    resp = requests.delete(f"{BASE_URL}/tasks/0")
    assert resp.status_code == 200
    data = resp.json()
    assert data["message"] == "Task deleted successfully"

    resp2 = requests.get(f"{BASE_URL}/tasks/0")
    assert resp2.status_code == 404
    data2 = resp2.json()
    assert data2["message"] == "Task not found"


def test_patch_task_not_found():
    resp = requests.patch(f"{BASE_URL}/tasks/9999", json={"title": "X"})
    assert resp.status_code == 404
    data = resp.json()
    assert data["message"] == "Task not found"


def test_delete_task_not_found():
    resp = requests.delete(f"{BASE_URL}/tasks/9999")
    assert resp.status_code == 404
    data = resp.json()
    assert data["message"] == "Task not found"
