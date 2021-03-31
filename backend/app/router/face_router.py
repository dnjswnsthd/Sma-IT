from fastapi import APIRouter, File, UploadFile, HTTPException

from models.visited import Visited
from crud import member_crud, visited_crud

from database.db import session

from utils.mask import mask_check
from utils.face import face_check
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

    if member_img == '얼굴인식 실패':
        raise HTTPException(status_code=400, detail="얼굴인식 실패")
    elif member_img == '등록된 회원이 아닙니다':
        raise HTTPException(status_code=400, detail=isMask)

    memberInfo = member_crud.get_member_by_image(session, member_img)
    # 입장 시간 저장
    visited_crud.create_visited(
        session, memberInfo.uuid, start_visted)
    # 아니 위에 visited 테이블 건드니깐 왜 이것도 바뀌냐고 망할 파이썬
    memberInfo = member_crud.get_member_by_image(session, member_img)
    face_data = dict(member=memberInfo, isMask=isMask)

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
        raise HTTPException(status_code=400, detail='등록된 회원이 아닙니다')

    member = member_crud.get_member_by_image(session, member_img)
    print(member.__dict__)
    face_data = dict(member=member)

    return face_data


@router.get("/onlymask/{img_path:path}", summary="마스크 인식")
async def mask_checking(img_path: str):
    print(img_path)
    mask_data = mask_check(img_path)
    return mask_data
