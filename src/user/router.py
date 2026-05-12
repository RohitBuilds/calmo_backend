from fastapi import APIRouter, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.user.models import User
from src.user import controller
from typing import List
from src.user.dtos import UserCreate, UserResponse, UserLogin
from src.utils.helper import is_authenticated

router = APIRouter(prefix="/users")

@router.post("/create",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(body:UserCreate,db:Session=Depends(get_db)):
    return controller.create_user(body,db)

@router.post("/login",status_code=status.HTTP_200_OK)
def login_user(body:UserLogin,db:Session=Depends(get_db)):
    return controller.login_user(body,db)

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, user: User = Depends(is_authenticated)):
    # is_authenticated confirms the token is valid before we blacklist it
    return controller.logout_user(request)
 
 
@router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(user: User = Depends(is_authenticated)):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username
    }

@router.get("/allusers",response_model=List[UserResponse],status_code=status.HTTP_200_OK)
def get_all_users(db:Session=Depends(get_db)):
    return controller.get_all_users(db)