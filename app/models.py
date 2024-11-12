from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.config import Base

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    # tasks = relationship("Task", back_populates="owner")
    # comments = relationship("Comment", back_populates="author")

# # Task Model
# class Task(Base):
#     __tablename__ = "tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True, nullable=False)
#     description = Column(Text, nullable=True)
#     status = Column(String, nullable=False, default="To Do")
#     priority = Column(Integer, nullable=True)
#     due_date = Column(DateTime, nullable=True)
#     created_at = Column(DateTime, server_default=func.now(), nullable=False)

#     # Foreign Key to User table
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     # Relationships
#     owner = relationship("User", back_populates="tasks")
#     comments = relationship("Comment", back_populates="task")
#     attachments = relationship("Attachment", back_populates="task")

# # Comment Model
# class Comment(Base):
#     __tablename__ = "comments"

#     id = Column(Integer, primary_key=True, index=True)
#     content = Column(Text, nullable=False)
#     timestamp = Column(DateTime, server_default=func.now(), nullable=False)

#     # Foreign Keys
#     task_id = Column(Integer, ForeignKey("tasks.id"))
#     author_id = Column(Integer, ForeignKey("users.id"))

#     # Relationships
#     task = relationship("Task", back_populates="comments")
#     author = relationship("User", back_populates="comments")

# # Attachment Model
# class Attachment(Base):
#     __tablename__ = "attachments"

#     id = Column(Integer, primary_key=True, index=True)
#     file_name = Column(String, nullable=False)
#     size = Column(Integer, nullable=False)
#     upload_status = Column(String, nullable=False)

#     # Foreign Key to Task table
#     task_id = Column(Integer, ForeignKey("tasks.id"))

#     # Relationships
#     task = relationship("Task", back_populates="attachments")
