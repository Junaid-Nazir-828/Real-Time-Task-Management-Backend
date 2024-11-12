from fastapi import FastAPI
from app.config import engine, Base
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Your route imports and router inclusions
from app.routers import views ,auth # tasks, attachments, websocket, 
app.include_router(auth.router, prefix="/auth", tags=["auth"])   # Removed the prefix="/auth"
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
# app.include_router(attachments.router, prefix="/attachments", tags=["attachments"])
# app.include_router(websocket.router, tags=["websocket"])
app.include_router(views.router, tags=["views"])
