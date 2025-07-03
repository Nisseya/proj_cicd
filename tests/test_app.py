import pytest
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:3001")

@pytest.fixture(scope="module")
def user_credentials():
    return {
        "email": "testuser@example.com",
        "password": "secure123",
        "name": "Test User"
    }

@pytest.fixture(scope="module")
def auth_token(user_credentials):
    reg_res = requests.post(f"{BASE_URL}/api/auth/register", json=user_credentials)
    assert reg_res.status_code in [200, 201, 400]

    login_res = requests.post(f"{BASE_URL}/api/auth/login", json={
        "email": user_credentials["email"],
        "password": user_credentials["password"]
    })
    assert login_res.status_code == 200
    return login_res.json()["token"]

def test_get_health():
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200
    assert res.json()["status"] == "OK"

def test_create_task(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    task = {
        "title": "Tâche testée",
        "description": "Une tâche créée depuis pytest",
        "priority": "high"
    }
    res = requests.post(f"{BASE_URL}/api/tasks", json=task, headers=headers)
    assert res.status_code == 201
    global TASK_ID
    TASK_ID = res.json()["id"]  # Stocker pour les tests suivants

def test_get_task_by_id(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.get(f"{BASE_URL}/api/tasks/{TASK_ID}", headers=headers)
    assert res.status_code == 200
    assert res.json()["id"] == TASK_ID

def test_update_task(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    update = {"status": "done"}
    res = requests.put(f"{BASE_URL}/api/tasks/{TASK_ID}", json=update, headers=headers)
    assert res.status_code == 200
    assert res.json()["status"] == "done"

def test_get_all_tasks(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.get(f"{BASE_URL}/api/tasks", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_delete_task(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.delete(f"{BASE_URL}/api/tasks/{TASK_ID}", headers=headers)
    assert res.status_code == 204

def test_get_users(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.get(f"{BASE_URL}/api/users", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_tasks_without_token():
    res = requests.get(f"{BASE_URL}/api/tasks")
    assert res.status_code == 401

def test_register_existing_user(user_credentials):
    res = requests.post(f"{BASE_URL}/api/auth/register", json=user_credentials)
    assert res.status_code == 400  # ou 409 si conflit

def test_delete_nonexistent_task(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    res = requests.delete(f"{BASE_URL}/api/tasks/fake-id-123", headers=headers)
    assert res.status_code in [404, 400]