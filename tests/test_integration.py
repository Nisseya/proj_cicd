import pytest
import requests

API_URL = "http://localhost:3001/api"  # à adapter si ton backend tourne sur un autre port

@pytest.fixture(scope="module")
def test_user():
    print("hello")
    return {
        "name": "Test Intégration",
        "email": "integration@test.com",
        "password": "integration123"
    }

@pytest.fixture(scope="module")
def auth_token(test_user):
    # Register or login
    resp = requests.post(f"{API_URL}/auth/register", json=test_user)
    if resp.status_code == 400:  # Already exists
        resp = requests.post(f"{API_URL}/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
    token = resp.json().get("token")
    assert token is not None
    return token

def test_get_users(auth_token):
    resp = requests.get(f"{API_URL}/users", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_create_task(auth_token):
    payload = {
        "title": "Tâche d’intégration",
        "description": "Créée par test d’intégration",
        "priority": "high",
        "assignedTo": None
    }
    resp = requests.post(f"{API_URL}/tasks", json=payload, headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "id" in data
    assert data["title"] == payload["title"]

def test_list_tasks(auth_token):
    resp = requests.get(f"{API_URL}/tasks", headers={
        "Authorization": f"Bearer {auth_token}"
    })
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_update_task(auth_token):
    # create
    task = requests.post(f"{API_URL}/tasks", json={
        "title": "To be updated",
        "priority": "low"
    }, headers={"Authorization": f"Bearer {auth_token}"}).json()

    task_id = task["id"]

    # update
    resp = requests.put(f"{API_URL}/tasks/{task_id}", json={
        "title": "Updated Title",
        "priority": "medium"
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Title"

def test_delete_task(auth_token):
    # create
    task = requests.post(f"{API_URL}/tasks", json={
        "title": "To be deleted",
        "priority": "low"
    }, headers={"Authorization": f"Bearer {auth_token}"}).json()

    # delete
    resp = requests.delete(f"{API_URL}/tasks/{task['id']}", headers={
        "Authorization": f"Bearer {auth_token}"
    })

    assert resp.status_code == 204  # ou in [200, 204] si incertitude
    # pas de resp.json() ici

