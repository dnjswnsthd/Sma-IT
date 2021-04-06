from fastapi import APIRouter, File, UploadFile, HTTPException

from models.visited import Visited
from crud import member_crud, visited_crud

from database.db import session

from utils.mask import mask_check
from utils.face import face_check

from sqlalchemy.exc import SQLAlchemyError

import base64

router = APIRouter()


@router.post("/mask/{start_visted}", summary="얼굴 인식 및 마스크 인식")
async def face_mask_checking(start_visted: str, file: UploadFile = File(...)):
    # 이미지 저장
    content = await file.read()
    with open(f'../img/cam_img/{file.filename}', 'wb') as fh:
        fh.write(content)

    isMask = mask_check("../img/cam_img/" + file.filename)
    # 얼굴인식 및 마스크 인식
    member_img = face_check(file.filename)

    print(isMask)
    print(member_img)
    if member_img == '얼굴인식 실패':
        if isMask == 'NO MASK':
            raise HTTPException(status_code=401, detail="얼굴인식 실패")
        elif isMask == 'MASK':
            raise HTTPException(status_code=400, detail="얼굴인식 실패")
    elif member_img == '등록된 회원이 아닙니다':
        if isMask == 'NO MASK':
            raise HTTPException(status_code=401, detail="Not Regist")
        elif isMask == 'MASK':
            raise HTTPException(status_code=400, detail="Not Regist")
    memberInfo = member_crud.get_member_by_image(session, member_img)
    # 입장 시간 저장
    try:
        visited_crud.create_visited(session, memberInfo.uuid, start_visted)
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="?? already registered")

    memberInfo = member_crud.get_member_by_image(session, member_img)

    # image 업로딩
    path = '../img/member_img/' + memberInfo.image
    base64_string = None
    with open(path, 'rb') as img:
        base64_string = base64.b64encode(img.read())

    face_data = dict(member=memberInfo, isMask=isMask, image=base64_string)

    return face_data


@router.post("/onlyface", summary="얼굴인식")
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

    member = member_crud.get_member_by_image(session, member_img)
    face_data = dict(member=member)

    return face_data


@router.get("/onlymask/{img_path:path}", summary="마스크 인식")
async def mask_checking(img_path: str):
    print(img_path)
    mask_data = mask_check("../img/cam_img/"+img_path)
    return mask_data
