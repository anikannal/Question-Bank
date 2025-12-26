# Team Task Manager - Full Stack Evaluation

Welcome to the Team Task Manager project! This is a simple task management application built with **Django** (Backend) and **Angular** (Frontend), using **PyMongo** to connect to **MongoDB**.

Your goal is to complete 3 specific tasks to improve the application.

## Setup

The project has been configured for easy setup.

1.  **Install Dependencies & Build**:
    ```bash
    ./install.sh
    ```

2.  **Run Application**:
    ```bash
    ./run.sh
    ```
    The full application (Backend API + Frontend UI) will be available at `http://127.0.0.1:8000`.

## The Tasks

### Task 1: Add "Priority" Field
**Context**: We need to know which tasks are urgent.
**Requirement**:
1.  Update the Backend (`core/views.py`) to include a `priority` field for tasks. Note: Since we are using PyMongo directly, you don't need to update models.py, but ensure the field is saved to MongoDB.
2.  Update the Frontend to display the priority of each task in the list.
3.  (Optional but recommended) Allow setting the priority when creating a task.

### Task 2: Fix "Mark as Completed" Bug
**Context**: Users are complaining that once they mark a task as completed, they cannot un-check it.
**Requirement**:
1.  Identify the bug in the backend or frontend logic (check `core/views.py` or frontend component).
2.  Fix it so that toggling the checkbox in the UI correctly updates the database state in both directions (True -> False and False -> True).

### Task 3: Filter by Assignee
**Context**: The "All Tasks" view is too cluttered. We need to filter tasks by the user they are assigned to.
**Requirement**:
1.  Update the `TaskList` view in `core/views.py`.
2.  It should accept an optional query parameter `owner_id`.
3.  If provided, return only tasks belonging to that user.

## Verification

We have provided a test suite to verify your work.
To run the tests:
```bash
pytest tests/evaluation_tests.py
```

**Passing all tests means you have successfully completed the evaluation.**

Good luck!
