from sqlalchemy import Column, Integer, String, Float, BLOB
from pydantic import BaseModel
from database import db


#Response Emotion Database
class ImagesTable(db.Base):
    __tablename__ = "images"
    uuid = Column(Integer, primary_key = True, autoincrement=True)
    member_uuid = Column(Integer, nullable=False)
    image = Column(BLOB, nullable=False)


#Request Emotion Database
class Images(BaseModel):
    member_uuid : int
    image : bytes
