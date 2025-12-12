from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    # Task 3: Candidate needs to implement filtering by assignee_id here
    return db.query(models.Task).offset(skip).limit(limit).all()

def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: schemas.TaskCreate):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not db_task:
        return None
    
    db_task.title = task_update.title
    db_task.description = task_update.description
    
    # BUG FOR TASK 2: 
    # Logic error: if task_update.is_completed is False, this block might be skipped 
    # or handled incorrectly depending on how the frontend sends data.
    # Actually, let's make it a subtle bug. 
    # If the user sends is_completed=False, but the DB has True, we want to allow un-checking.
    # But let's say we accidentally check `if task_update.is_completed:` which fails for False.
    
    if task_update.is_completed:
        db_task.is_completed = task_update.is_completed
        
    db.commit()
    db.refresh(db_task)
    return db_task
