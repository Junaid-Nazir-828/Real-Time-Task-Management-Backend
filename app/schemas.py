from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# Task Schemas
# class TaskBase(BaseModel):
#     title: str
#     description: Optional[str] = None
#     status: str = "To Do"        # Default status
#     priority: Optional[int] = Field(None, ge=1, le=5, description="Priority level from 1 to 5")
#     due_date: Optional[datetime] = None

# class TaskCreate(TaskBase):
#     pass

# class TaskRead(TaskBase):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True


# # Comment Schemas
# class CommentBase(BaseModel):
#     content: str

# class CommentCreate(CommentBase):
#     pass

# class CommentRead(CommentBase):
#     id: int
#     author: str
#     timestamp: datetime

#     class Config:
#         orm_mode = True


# # Attachment Schemas
# class AttachmentBase(BaseModel):
#     file_name: str
#     size: int
#     upload_status: str

# class AttachmentCreate(AttachmentBase):
#     pass

# class AttachmentRead(AttachmentBase):
#     id: int
#     associated_task_id: int

#     class Config:
#         orm_mode = True
