import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app, get_db
from backend.models import Base

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200, "Should be able to create a user"
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_task_1_priority_field():
    """
    Task 1: Add 'priority' field.
    This test checks if we can create a task with a priority field and retrieve it.
    """
    # Create user
    user_res = client.post("/users/", json={"email": "prio@test.com", "password": "pw"})
    user_id = user_res.json().get("id") or 1

    # Try to create task with priority
    response = client.post(
        f"/users/{user_id}/tasks/",
        json={
            "title": "Priority Task", 
            "priority": "High" # This field doesn't exist yet
        },
    )
    
    # If the candidate hasn't implemented it, this might ignore the field or fail validation
    # We expect it to succeed AND return the priority field
    if response.status_code != 200:
        pytest.fail("Failed to create task. Did you update the schema?")
        
    data = response.json()
    if "priority" not in data:
        pytest.fail("Task response does not contain 'priority' field.")
        
    assert data["priority"] == "High", "Priority was not saved/returned correctly."

def test_task_2_completion_bug():
    """
    Task 2: Fix 'Mark as Completed' bug.
    The bug prevents unchecking a task (setting is_completed to False).
    """
    # Create user
    user_res = client.post("/users/", json={"email": "bug@test.com", "password": "pw"})
    user_id = user_res.json().get("id") or 1

    # Create task (default is_completed=False)
    create_res = client.post(
        f"/users/{user_id}/tasks/",
        json={"title": "Bug Task"}
    )
    task_id = create_res.json()["id"]

    # Set to True
    update_res = client.put(f"/tasks/{task_id}", json={"title": "Bug Task", "is_completed": True})
    assert update_res.json()["is_completed"] is True, "Failed to set is_completed to True"

    # Set back to False (THIS IS THE BUG)
    update_res_2 = client.put(f"/tasks/{task_id}", json={"title": "Bug Task", "is_completed": False})
    
    assert update_res_2.json()["is_completed"] is False, "Failed to set is_completed back to False. Did you fix the bug in crud.py?"

def test_task_3_filter_by_assignee():
    """
    Task 3: Filter by Assignee.
    """
    # Create two users
    u1 = client.post("/users/", json={"email": "u1@test.com", "password": "pw"}).json()
    u2 = client.post("/users/", json={"email": "u2@test.com", "password": "pw"}).json()

    # Create tasks for u1
    client.post(f"/users/{u1['id']}/tasks/", json={"title": "U1 Task 1"})
    client.post(f"/users/{u1['id']}/tasks/", json={"title": "U1 Task 2"})

    # Create tasks for u2
    client.post(f"/users/{u2['id']}/tasks/", json={"title": "U2 Task 1"})

    # Filter for U1
    # Note: The candidate might implement this as ?assignee_id=X or ?owner_id=X. 
    # The instructions say "assignee_id".
    res_u1 = client.get(f"/tasks/?assignee_id={u1['id']}")
    
    # If parameter is ignored, it returns all 3 tasks
    tasks = res_u1.json()
    assert len(tasks) == 2, f"Expected 2 tasks for user 1, got {len(tasks)}. Is the filter working?"
    assert all(t["owner_id"] == u1["id"] for t in tasks)

    # Filter for U2
    res_u2 = client.get(f"/tasks/?assignee_id={u2['id']}")
    tasks_2 = res_u2.json()
    assert len(tasks_2) == 1
    assert tasks_2[0]["title"] == "U2 Task 1"
