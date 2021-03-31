from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database import db


# Response Visited Database
class VisitedTable(db.Base):
    __tablename__ = "visited"
    visited_id = Column(Integer, primary_key=True, autoincrement=True)  
    start_visit = Column(String(20))
    end_visit = Column(String(20))
    uuid = Column(Integer)

# Request Visited Database
class Visited(BaseModel):
    uuid : int
    start_visit: str


    



