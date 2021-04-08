from fastapi import APIRouter, File, UploadFile, HTTPException

from models.visited import Visited
from crud import member_crud, visited_crud

from database.db import session

from utils.mask import mask_check
from utils.face import face_check

import base64

router = APIRouter()


@router.post("/onlyface", summary="얼굴 인식을 통한 고객 정보 제공")
async def face_checking(file: UploadFile = File(...)):
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
    # 얼굴 인식으로 찾은 이미지를 기반으로 고객 정보 가져오기
    member = member_crud.get_member_by_image(session, member_img)
    # image 업로딩
    path = '../img/member_img/' + member.image
    base64_string = None
    with open(path, 'rb') as img:
        base64_string = base64.b64encode(img.read())
    # 고객 정보와 이미지 제공
    face_data = dict(member=member, image=base64_string)

    return face_data


@router.post("/onlymask", summary="마스크 착용 여부 검사")
async def mask_checking(file: UploadFile = File(...)):
    # 이미지 저장
    content = await file.read()
    with open(f'../img/cam_img/{file.filename}', 'wb') as fh:
        fh.write(content)
    # 가져온 이미지를 통해 마스크 착용 여부 검사
    mask_data = mask_check("../img/cam_img/" + file.filename)
    return mask_data
