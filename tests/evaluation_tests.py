import sys
import os

# Check if run directly
if __name__ == "__main__":
    print("\n[ERROR] Do not run this file directly with 'python'.")
    print("Please run tests using 'pytest' from the project root directory:")
    print("    pytest tests/evaluation_tests.py\n")
    sys.exit(1)

import pytest
from rest_framework.test import APIClient
from core.utils import users_collection, tasks_collection
from bson import ObjectId

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(autouse=True)
def clean_db():
    users_collection.delete_many({})
    tasks_collection.delete_many({})
    yield

@pytest.mark.django_db
def test_create_user(api_client):
    response = api_client.post(
        "/users/",
        {"email": "test@example.com", "is_active": True},
        format='json'
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.django_db
def test_task_1_priority_field(api_client):
    user_res = api_client.post("/users/", {"email": "prio@test.com", "is_active": True}, format='json')
    user_id = user_res.json().get("id")

    response = api_client.post(
        "/tasks/",
        {
            "title": "Priority Task",
            "owner_id": user_id,
            "priority": "High"
        },
        format='json'
    )
    assert response.status_code == 201
    data = response.json()
    assert data.get("priority") == "High"

@pytest.mark.django_db
def test_task_2_completion_bug(api_client):
    user_res = api_client.post("/users/", {"email": "bug@test.com"}, format='json')
    user_id = user_res.json().get("id")

    create_res = api_client.post(
        "/tasks/",
        {"title": "Bug Task", "owner_id": user_id},
        format='json'
    )
    task_id = create_res.json()["id"]

    # Initial state
    assert create_res.json()["is_completed"] is False

    # Set to True
    update_res = api_client.put(f"/tasks/{task_id}/", {"title": "Bug Task", "is_completed": True}, format='json')
    assert update_res.status_code == 200
    assert update_res.json()["is_completed"] is True

    # Set back to False
    update_res_2 = api_client.put(f"/tasks/{task_id}/", {"title": "Bug Task", "is_completed": False}, format='json')
    assert update_res_2.status_code == 200
    assert update_res_2.json()["is_completed"] is False

@pytest.mark.django_db
def test_task_3_filter_by_assignee(api_client):
    u1 = api_client.post("/users/", {"email": "u1@test.com"}, format='json').json()
    u2 = api_client.post("/users/", {"email": "u2@test.com"}, format='json').json()

    api_client.post("/tasks/", {"title": "U1 Task 1", "owner_id": u1['id']}, format='json')
    api_client.post("/tasks/", {"title": "U1 Task 2", "owner_id": u1['id']}, format='json')
    api_client.post("/tasks/", {"title": "U2 Task 1", "owner_id": u2['id']}, format='json')

    res_u1 = api_client.get(f"/tasks/?owner_id={u1['id']}")
    assert res_u1.status_code == 200
    assert len(res_u1.json()) == 2
    for task in res_u1.json():
        assert task['owner_id'] == u1['id']
