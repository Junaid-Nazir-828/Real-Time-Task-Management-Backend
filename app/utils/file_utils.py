import os
import asyncio
from fastapi import UploadFile
from fastapi.responses import JSONResponse

CHUNK_SIZE = 1024 * 1024  # 1MB chunks

# Ensure the upload folder exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

async def save_file_chunk(file_name: str, file: UploadFile):
    """
    Handles saving a chunk of the file to disk.
    Appends chunks to the file being uploaded.
    """
    file_location = os.path.join(UPLOAD_FOLDER, file_name)
    try:
        # Open the file and append the chunk
        with open(file_location, "ab") as f:
            chunk = await file.read()
            f.write(chunk)
            await asyncio.sleep(0.5)  # Simulate delay for tracking progress
        return {"status": "success", "chunk_size": len(chunk)}
    except Exception as e:
        raise Exception(f"Error uploading file chunk: {e}")

def create_empty_file(file_name: str):
    """
    Create a placeholder file when starting the upload (to prevent overwriting existing files).
    """
    try:
        file_location = os.path.join(UPLOAD_FOLDER, file_name)
        # Create an empty file to hold the incoming chunks
        with open(file_location, "wb") as f:
            pass
        return {"status": "success", "file_name": file_name}
    except Exception as e:
        raise Exception(f"Error initializing file upload: {e}")
