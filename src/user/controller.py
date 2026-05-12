from fastapi import APIRouter, Depends ,Request 
from  pwdlib import PasswordHash
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.utils.db import get_db
from src.user.models import User
from src.user.dtos import UserCreate, UserResponse, UserLogin   
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError  
from datetime import datetime,timedelta
from src.utils.setting import settings
from src.utils.blacklist import add_to_blacklist

passwordHash=PasswordHash.recommended()

def get_password_hash(password):
    return passwordHash.hash(password)

def verify_password(plain_password,hashed_password):
    return passwordHash.verify(plain_password,hashed_password)

def create_user(body:UserCreate,db:Session):
    data=body.model_dump()

    if db.query(User).filter(User.email==data['email']).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this email already exists")
    
    if db.query(User).filter(User.username==data['username']).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with this username already exists")
    
    hashed_password=get_password_hash(body.password)    

    new_user=User(
        email=data['email'],
        name=data['name'],
        username=data['username'],
        hashed_password=hashed_password   
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(body:UserLogin,db:Session):
    data=body.model_dump()
    user=db.query(User).filter(User.email==data['email']).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    if not passwordHash.verify(data['password'],user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid password")
    
    exp_time=datetime.utcnow()+timedelta(minutes=settings.EXP_TIME)
    token=jwt.encode({"id": user.id,"exp":exp_time},settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return {"token": token}

def logout_user(request: Request):
    # Extract the raw token from the Authorization header and blacklist it
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.split(" ")[-1]
 
    if token:
        add_to_blacklist(token)
 
    return {"message": "Logged out successfully"}

def get_all_users(db:Session):
    users=db.query(User).all()
    return users