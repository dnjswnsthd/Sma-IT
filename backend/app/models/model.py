from sqlalchemy import Column, Integer, String, Boolean, Float
from pydantic import BaseModel
from database import db

# Response Member Database
class MemberTable(db.Base):
    __tablename__ = 'member'
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    age = Column(Integer, nullable=False)
    interests = Column(String(80))
    requirements = Column(String(70))
    join_date = Column(String(30), nullable=False)
    image = Column(String(300), nullable=False)

# Request Member Database
class Member(BaseModel):
    name: str
    age: int
    interests: str
    requirements: str
    image: str


# Response Visited Database
class VisitedTable(db.Base):
    __tablename__ = "visited"
    uuid = Column(Integer, primary_key=True)
    start_visit = Column(String(20))
    end_visit = Column(String(20))

# Request Visited Database
class Visited(BaseModel):
    uuid : int
    start_visit : str
    end_visit : str

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

    



