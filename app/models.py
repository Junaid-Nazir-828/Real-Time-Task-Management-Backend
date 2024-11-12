from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from uuid import uuid4
from app.config import Base
import enum

# Enum for task status
class TaskStatus(str, enum.Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

def generate_task_id():
    return str(uuid4())

# Task Model
class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, default=generate_task_id)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer)
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)

    # Foreign key and relationship with User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="tasks")

    # Relationship with attachments
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")

# Attachment Model (File info)
class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer)
    upload_status = Column(String, default="Not Started")
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)

    # Relationship with Task
    task = relationship("Task", back_populates="attachments")

# Updating the User model to include a relationship with tasks
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship with Task
    tasks = relationship("Task", back_populates="user")
