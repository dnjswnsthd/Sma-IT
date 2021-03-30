from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from database import db


#Response Emotion Database
class EmotionTable(db.Base):
    __tablename__ = "emotion"
    uuid = Column(Integer, primary_key = True)
    anger = Column(Float)
    contempt = Column(Float)
    disgust = Column(Float)
    fear = Column(Float)
    happiness = Column(Float)
    neutral = Column(Float)
    sadness = Column(Float)
    surprise = Column(Float)
    end_visit = Column(String(30), primary_key = True)

#Request Emotion Database
class Emotion(BaseModel):
    uuid : int
    anger : float
    contempt : float
    disgust : float
    fear : float
    happiness : float
    neutral : float
    sadness : float
    surprise : float
    end_visit : str
