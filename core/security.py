import os
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, Request
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models
from database import get_db

SECRET_KEY = os.environ.get("JWT_SECRET", "super-secret-luxe-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

security = HTTPBearer(auto_error=False)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security) 
):
    # Check for credentials from Authorization header first
    token = None
    if credentials:
        token = credentials.credentials
    
    # Fallback to Cookie (luxe_token)
    if not token:
        token = request.cookies.get("luxe_token")

    if not token:
        throw_auth_error("Not authenticated")
    
    try:
        # Decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            throw_auth_error("Invalid session token.")
    except jwt.PyJWTError:
        throw_auth_error("Token validation failed.")
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or user.is_deleted:
        throw_auth_error("User not found or account is deleted.")
    return user

def throw_auth_error(detail: str):
     raise HTTPException(status_code=401, detail=detail)
