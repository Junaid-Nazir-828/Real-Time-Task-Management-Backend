from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from fastapi import Request, HTTPException

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


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
    
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    print(f"Token: {token}")  # Debugging line to check the token
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        if token.startswith("Bearer "):
            token = token[7:]
        
        user = decode_access_token(token)
        print(f"User: {user}")  # Debugging line to check the decoded user
    except Exception as e:
        print(f"Error: {e}")  # Log error message
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user

