from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.models import Task as TaskModel, Attachment
from app.schemas import TaskCreate, Task
from app.dependencies import get_db
from app.utils.auth_utils import get_current_user
from app.utils.file_utils import create_empty_file, save_file_chunk  # Import the utility functions
import logging
import os
# Create a logger
logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Create task in database
        db_task = TaskModel(**task.dict())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        # Handle file attachment
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())  # Write file as a whole

        # Create attachment entry in the database
        attachment = Attachment(file_name=file.filename, task_id=db_task.id)
        db.add(attachment)
        db.commit()

        # Update task status to 'Done' after file upload
        db_task.status = "Done"
        db.commit()

        return db_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {e}")
    
# GET route for retrieving all tasks
@router.get("/")
async def get_tasks(db: Session = Depends(get_db)):
    try:
        # Query all tasks from the database
        tasks = db.query(Task).all()
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {e}")