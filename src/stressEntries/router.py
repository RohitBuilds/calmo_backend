from fastapi import APIRouter, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.stressEntries.models import StreeEntries
from src.stressEntries import controller
from typing import List
from src.stressEntries.dtos import StressInput,StressOutput
from src.utils.helper import is_authenticated
from src.user.models import User
router=APIRouter(prefix="/stress")

@router.post("/createstressentries",response_model=StressOutput,status_code=status.HTTP_201_CREATED)
def createEntries(body:StressInput,db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.createEntries(body,db,user)

@router.get("/getallentries",response_model=List[StressOutput],status_code=status.HTTP_200_OK)
def getallEntries(db:Session=Depends(get_db),user:User=Depends(is_authenticated)):
    return controller.getallEntries(db,user)

