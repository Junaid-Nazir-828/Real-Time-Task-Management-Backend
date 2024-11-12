from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

# Attachment Schemas
class AttachmentBase(BaseModel):
    file_name: str
    file_size: Optional[int] = None
    upload_status: Optional[str] = None

class AttachmentCreate(AttachmentBase):
    task_id: str

class Attachment(AttachmentBase):
    id: int
    task_id: str

    class Config:
        orm_mode = True

# Task Schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "To Do"
    priority: Optional[int] = 1
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str
    attachments: List[Attachment] = []
    user_id: int

    class Config:
        orm_mode = True
