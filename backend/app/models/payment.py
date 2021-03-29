from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from pydantic import BaseModel
from database import db

class PaymentTable(db.Base):
    __tablename__ = 'payment'
    uuid = Column(Integer, primary_key=True, autoincrement=False)
    card_num = Column(BigInteger, nullable=False)
    card_name = Column(String(45), nullable=False)

class Payment(BaseModel):
    uuid: int
    card_num: int
    card_name: str