from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from fastapi import Request
import logging
from app.models import User  # Adjust the import path based on your project structure
from app.dependencies import get_db  # Import your database session function
from sqlalchemy.orm import Session
from fastapi import Depends
# Load environment variables
load_dotenv()

# Load and validate environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is missing!")

if not ALGORITHM:
    raise ValueError("ALGORITHM environment variable is missing!")

# Create a logger
logger = logging.getLogger("auth_utils")
logging.basicConfig(level=logging.INFO)  # Set logging level as needed

def create_access_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token")

def get_user_by_username(username: str, db: Session) -> User:
    # Query the database for the user
    return db.query(User).filter(User.username == username).first()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get("access_token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        if token.startswith("Bearer "):
            token = token[7:]  # Strip "Bearer " prefix

        username = decode_access_token(token)
        user = get_user_by_username(username, db)  # Fetch the user from the database
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    return user
