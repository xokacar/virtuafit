from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Workout(Base):
    __tablename__ = 'workouts'
    id = Column(Integer, primary_key=True)
    user = Column(String(50), nullable=False)
    workout_type = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)