from fastapi import FastAPI
from app.config import engine, Base
from app import models
from app.routers import file, views, auth , task # , notifications
from app.routers import websocket

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(views.router, tags=["views"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
# app.include_router(notifications.router, tags=["notifications"])
app.include_router(file.router, tags=["file_upload"])
app.include_router(websocket.websocket_router)
