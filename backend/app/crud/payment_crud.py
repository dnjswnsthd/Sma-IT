from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.payment import Payment, PaymentTable


# 고객의 uuid를 기반으로 등록 된 카드 정보 제공
def select_cardInfo_by_UUID(db: Session, uuid: int):
    return db.query(PaymentTable).filter(PaymentTable.uuid == uuid).first()


# 고객의 카드 정보 등록
def insert_cardInfo(db: Session, payment: Payment):
    db_payment = PaymentTable()
    db_payment.uuid = payment.uuid
    db_payment.card_num = payment.card_num
    db_payment.card_name = payment.card_name
    try:
        db.add(db_payment)
        db.commit()
        db.refresh(db_payment)
    except:
        db.rollback()
        raise SQLAlchemyError

    return db_payment
