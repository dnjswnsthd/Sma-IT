from fastapi import APIRouter
from crud import payment_crud as crud
from models.payment import Payment
from database.db import session

router = APIRouter()


@router.post("/register")
async def insert_cardInfo(payment: Payment):
    db_payment = crud.select_cardInfo_by_UUID(session, payment.uuid)
    if db_payment:
        raise HTTPException(status_code=400, detail="?? already registered")
    
    db_payment = crud.insert_cardInfo(session, payment)
    if db_payment is None:
        raise HTTPException(status_code=400, detail="Insert fail")

    return db_payment