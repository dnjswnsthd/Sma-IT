from fastapi import APIRouter, HTTPException, File, UploadFile
from crud import member_crud, payment_crud
from models.payment import Payment
from database.db import session

from utils.face import face_check

from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()


@router.post("/register", summary="결제 정보 등록")
async def insert_cardInfo(payment: Payment):
    try:
        # 결제 정보 등록
        db_payment = payment_crud.insert_cardInfo(session, payment)
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Insert fail")

    return db_payment


@router.post("/", summary="얼굴 인식 기반 결제")
async def get_cardInfo(file: UploadFile = File(...)):
    # 이미지 저장
    content = await file.read()
    with open(f'../img/cam_img/{file.filename}', 'wb') as fh:
        fh.write(content)

    # 얼굴인식
    member_img = face_check(file.filename)
    if member_img == '얼굴인식 실패':
        raise HTTPException(status_code=400, detail="얼굴인식 실패")
    elif member_img == '등록된 회원이 아닙니다':
        raise HTTPException(status_code=400, detail='Not Regist')
    # 얼굴 인식으로 찾은 이미지를 통해 고객 정보 가져오기
    member = member_crud.get_member_by_image(session, member_img)
    # 등록된 고객의 결제 정보 가져오기
    payment = payment_crud.select_cardInfo_by_UUID(session, member.uuid)

    return payment
