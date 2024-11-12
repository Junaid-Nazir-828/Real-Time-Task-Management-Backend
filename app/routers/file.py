from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import asyncio  # Import asyncio for adding delays
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
CHUNK_SIZE = 1024 * 1024  # 1MB chunks

@router.post("/start-upload")
async def start_file_upload(file: UploadFile = File(...)):
    """
    Endpoint to initialize the file upload. This will create a placeholder file for the chunks.
    """
    try:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        # Create an empty file to hold incoming chunks
        with open(file_location, "wb") as f:
            pass
        return {"status": "success", "file_name": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error initializing file upload: {e}")

@router.put("/upload-chunk/{file_name}")
async def upload_file_chunk(file_name: str, file: UploadFile = File(...)):
    """
    Endpoint to handle the upload of a file chunk.
    """
    file_location = os.path.join(UPLOAD_FOLDER, file_name)
    try:
        # Append the incoming chunk to the existing file
        with open(file_location, "ab") as f:
            chunk = await file.read()
            f.write(chunk)
            await asyncio.sleep(0.5)  # Introduce a small delay to track progress
        return {"status": "success", "chunk_size": len(chunk)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file chunk: {e}")

@router.get("/list")
async def list_files():
    """List all files in the uploads directory."""
    try:
        files = os.listdir(UPLOAD_FOLDER)
        print(files)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {e}")

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    """Download a specified file from the uploads directory."""
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=file_name)
    else:
        raise HTTPException(status_code=404, detail="File not found")
