# Team Task Manager - Full Stack Evaluation

Welcome to the Team Task Manager project! This is a simple task management application built with **Django** (Backend) and **Angular** (Frontend), using **MongoDB** as the database.

Your goal is to complete 3 specific tasks to improve the application.

## Setup

1.  **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```
    The API will run at `http://127.0.0.1:8000`.

2.  **Frontend**:
    ```bash
    cd frontend
    npm install
    npm start
    ```
    The UI will run at `http://localhost:4200`.

## The Tasks

### Task 1: Add "Priority" Field
**Context**: We need to know which tasks are urgent.
**Requirement**:
1.  Update the Backend (`backend/core/models.py`, `backend/core/serializers.py`) to include a `priority` field for tasks. It should store values like "Low", "Medium", "High".
2.  Update the Frontend to display the priority of each task in the list.
3.  (Optional but recommended) Allow setting the priority when creating a task.

### Task 2: Fix "Mark as Completed" Bug
**Context**: Users are complaining that once they mark a task as completed, they cannot un-check it.
**Requirement**:
1.  Identify the bug in the backend or frontend logic (check `backend/core/views.py` or frontend component).
2.  Fix it so that toggling the checkbox in the UI correctly updates the database state in both directions (True -> False and False -> True).

### Task 3: Filter by Assignee
**Context**: The "All Tasks" view is too cluttered. We need to filter tasks by the user they are assigned to.
**Requirement**:
1.  Update the `TaskViewSet` in `backend/core/views.py`.
2.  It should accept an optional query parameter `owner_id`.
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
