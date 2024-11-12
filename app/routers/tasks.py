from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import TaskCreate, TaskRead
from app.crud import create_task, get_tasks
from typing import List

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
async def read_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)


@router.post("/", response_model=TaskRead)
async def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)
