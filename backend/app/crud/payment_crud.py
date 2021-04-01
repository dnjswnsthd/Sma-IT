from sqlalchemy.orm import Session

from models.payment import Payment, PaymentTable


def select_cardInfo_by_UUID(db: Session, uuid: int):
    return db.query(PaymentTable).filter(PaymentTable.uuid == uuid).first()


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
        raise

    return db_payment
