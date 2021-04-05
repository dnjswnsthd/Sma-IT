from fastapi import APIRouter, HTTPException
from crud import payment_crud as crud
from models.payment import Payment
from database.db import session

from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.post("/register")
async def insert_cardInfo(payment: Payment):
    try:
        db_payment = crud.insert_cardInfo(session, payment)
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Insert fail")

    return db_payment


@router.get("/{member_uuid}")
async def get_cardInfo(member_uuid: int):
    payment = crud.select_cardInfo_by_UUID(session, member_uuid)
    return payment
