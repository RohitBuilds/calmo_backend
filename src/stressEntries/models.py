from sqlalchemy import Column,Integer,String,DateTime,Float,ForeignKey,JSON,Text
from datetime import datetime
from src.utils.db import Base

class StreeEntries(Base):
    __tablename__='stressEntries'
    id=Column(Integer,primary_key=True,index=True)
    sleepDuration=Column(Float,nullable=False,index=True)
    physical_activity_level=Column(Float,nullable=False,index=True)
    quality_of_sleep=Column(Float,nullable=False,index=True)
    heart_rate=Column(Float,nullable=False,index=True)
    daily_steps=Column(Integer,nullable=False,index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    stress_score = Column(Float)
    recommendations = Column(JSON)
    motivation = Column(Text)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))
    