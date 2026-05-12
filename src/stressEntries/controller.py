from fastapi import APIRouter, Depends  
from  pwdlib import PasswordHash
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.utils.db import get_db
from src.stressEntries.models import StreeEntries
from src.user.models import User
from src.stressEntries.dtos import StressInput,StressOutput  
import jwt
from jwt.exceptions import ExpiredSignatureError,InvalidTokenError  
from datetime import datetime,timedelta
from src.utils.setting import settings
from src.ml.predict import predict_stress
from src.AI.reccomendation import (generate_recommendations)

def createEntries(body: StressInput, db: Session, user: User):

    score = predict_stress(body)
    
    ai_response = generate_recommendations(
        body,
        score
    ) 

    new_entry = StreeEntries(
        sleepDuration=body.sleepDuration,
        quality_of_sleep=body.quality_of_sleep,
        physical_activity_level=body.physical_activity_level,
        heart_rate=body.heart_rate,
        daily_steps=body.daily_steps,
        stress_score=score,
        recommendations=ai_response["recommendations"],
        motivation=ai_response["motivation"],
        user_id=user.id
    )
    # ai_response = generate_recommendations(
    #     body,
    #     score
    # )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {
        "stress_score": score,
        "recommendations": ai_response["recommendations"],
        "motivation": ai_response["motivation"],
        "user_id": user.id,
        "data": new_entry
    }

def getallEntries(db:Session,user:User):
    data=db.query(StreeEntries).filter(StreeEntries.user_id == user.id).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="not authenticated")
    return data
    