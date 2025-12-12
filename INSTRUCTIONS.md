# Team Task Manager - Full Stack Evaluation

Welcome to the Team Task Manager project! This is a simple task management application built with **FastAPI** (Backend) and **React** (Frontend).

Your goal is to complete 3 specific tasks to improve the application.

## Setup

1.  **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
    The API will run at `http://localhost:8000`.

2.  **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
    The UI will run at `http://localhost:5173`.

## The Tasks

### Task 1: Add "Priority" Field
**Context**: We need to know which tasks are urgent.
**Requirement**:
1.  Update the Backend (`models.py`, `schemas.py`) to include a `priority` field for tasks. It should store values like "Low", "Medium", "High".
2.  Update the Frontend to display the priority of each task in the list.
3.  (Optional but recommended) Allow setting the priority when creating a task.

### Task 2: Fix "Mark as Completed" Bug
**Context**: Users are complaining that once they mark a task as completed, they cannot un-check it.
**Requirement**:
1.  Identify the bug in `backend/crud.py`.
2.  Fix it so that toggling the checkbox in the UI correctly updates the database state in both directions (True -> False and False -> True).

### Task 3: Filter by Assignee
**Context**: The "All Tasks" view is too cluttered. We need to filter tasks by the user they are assigned to.
**Requirement**:
1.  Update the `GET /tasks/` endpoint in `backend/main.py` and `backend/crud.py`.
2.  It should accept an optional query parameter `assignee_id`.
3.  If provided, return only tasks belonging to that user.

## Verification

We have provided a test suite to verify your work.
To run the tests:
```bash
# From the root directory
pytest tests/evaluation_tests.py
```

**Passing all tests means you have successfully completed the evaluation.**

Good luck!
