from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from .db import Base
from .db import ENGINE


class MemberTable(Base):
    __tablename__ = 'member'
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False)
    age = Column(Integer, nullable=False)
    interests = Column(String(80))
    requirements = Column(String(70))
    join_date = Column(String(30), nullable=False)
    image = Column(String(300), nullable=False)

class Member(BaseModel):
    name: str
    age: int
    interests: str
    requirements: str
    image: str
