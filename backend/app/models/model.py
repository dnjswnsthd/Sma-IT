from sqlalchemy import Column, Integer, String, Boolean
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
    uuid : int
    name: str
    age: int
    interests: str
    requirements: str
    image: str

# Response Negative Database
class NegativeTable(db.Base):
    __tablename__ = 'negative'
    uuid = Column(Integer, primary_key=True)
    anger = Column(Integer)
    aversion = Column(Integer)
    sad = Column(Integer)
    fear = Column(Integer)
    anxiety = Column(Integer)

# Request Negative Database
class Negative(BaseModel):
    uuid : int
    anger: int
    aversion: int
    sad: int
    fear: int
    anxiety: int

# Response Positive Database
class PositiveTable(db.Base):
    __tablename__ = "positive"
    uuid = Column(Integer, primary_key=True)
    satisfaction = Column(Integer)
    comfortable = Column(Integer)
    joy = Column(Integer)
    funny = Column(Integer)
    pride = Column(Integer)

# Request Positive Database
class Positive(BaseModel):
    uuid: int
    satisfaction: int
    comfortable : int
    joy : int
    funny: int
    pride: int
    
# Response Satisfaction Database
class SatisfactiontTable(db.Base):
    __tablename__ = "satisfaction"
    uuid = Column(Integer, primary_key=True)
    exist = Column(Boolean, nullable=False, default=False)

# Request Satisfaction Database
class Satisfaction(BaseModel):
    uuid : int
    exist : bool

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


    



