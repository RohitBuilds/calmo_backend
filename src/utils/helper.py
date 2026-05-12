from fastapi import HTTPException,Request,status,Depends
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError  
from src.utils.setting import settings
from sqlalchemy.orm import Session
from src.user.models import User
from src.utils.db import get_db
from src.utils.blacklist import is_blacklisted

passwordHash=PasswordHash.recommended() 

def is_authenticated(request:Request,db:Session=Depends(get_db)):
    try: 
       token=request.headers.get("Authorization")
       if not token:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token missing")
       token=token.split(" ")[-1]

       if is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been invalidated. Please log in again."
            )
       
       data=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
       user_id=data.get("id")
       user=db.query(User).filter(User.id==user_id).first()
       if not user:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
       return user
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")