from pydantic import BaseModel
from typing import List
class StressInput(BaseModel):
    sleepDuration:float
    physical_activity_level:float
    quality_of_sleep:float
    heart_rate:float
    daily_steps:int
    

class StressOutput(BaseModel):
    stress_score : float
    recommendations: List[str]
    motivation: str
    user_id:int 