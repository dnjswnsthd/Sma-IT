from fastapi import APIRouter, File, UploadFile, HTTPException

from models.member import Member, UpdateMember
from models.emotion import Emotion

from crud import member_crud as crud
from crud import visited_crud
from database.db import session

from utils.face import face_image
from sqlalchemy.exc import SQLAlchemyError

import base64
import datetime

router = APIRouter()


@router.get("/", summary="고객 정보 가져오기(start ~ limit 까지 제공)")
async def read_members_limit(start: int = 0, limit: int = 10):
    # start ~ limit 까지의 고객 정보 가져오기
    members = crud.get_members(session, start, limit)
    # 고객 정보에 해당하는 프로필 사진 가져오기
    images = []
    for member in members:
        path = '../img/member_img/' + member['image']
        # 사진을 base64로 encoding 하여 제공
        with open(path, 'rb') as img:
            base64_string = base64.b64encode(img.read())
            images.append(base64_string)
    # 데이터를 dict 형으로 제공
    data = dict(members=members, images=images)

    return data


@router.get("/{member_uuid}", summary="uuid 기반 특정 고객 정보 제공")
async def read_member(member_uuid: int):
    # 고객 정보 가져오기
    member = crud.get_member_by_uuid(session, member_uuid)
    return member


@router.post("/", summary="고객 정보 등록")
async def create_members(member: Member):
    # 등록되있는지 체크
    db_member = crud.get_member_by_name(session, member.name)
    # 이미 가입된 회원
    if db_member:
        raise HTTPException(status_code=400, detail="?? already registered")

    # 시간생성
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # 등록
        db_member = crud.create_member(session, member, now)
        # image 등록
        db_member = crud.update_image_member(
            session, db_member, db_member.uuid)
        # 고객 등록 시 방문 시간 역시 업데이트(고객 등록을 위해서는 매장을 방문했다고 가정)
        visited_crud.create_visited(
            session, db_member.uuid, db_member.join_date)
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Creation failure")

    db_member = crud.get_member_by_name(session, member.name)
    return db_member


@router.post("/image/{image}", summary="고객 인식을 위한 사진 등록 및 수정")
async def create_members_img(image: str, file: UploadFile = File(...)):
    # 이미지 저장
    content = await file.read()
    with open(f'../img/member_img/{image}', 'wb') as fh:
        fh.write(content)
    try:
        face_image(image)
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="image Creation failure")
        
    return "OK"


@router.put("/", summary="고객 정보 수정")
async def update_members(member: UpdateMember):
    # 수정할 고객 정보 가져오기
    db_member = crud.get_member_by_uuid(session, member.uuid)
    # 고객 정보가 없다면 error 400 error 발생
    if db_member is None:
        raise HTTPException(status_code=400, detail="No members")
    # 고객 정보 수정
    db_member = crud.update_member(session, db_member, member)

    return db_member


@router.delete("/{member_uuid}", summary="고객 정보 삭제")
async def delete_members(member_uuid: int):
    try:
        # 고객 정보 삭제 진행
        db_member = crud.delete_member_by_uuid(session, member_uuid)
        # 삭제 된 컬럼이 없다면 삭제 실패(고객 정보가 없거나...)
        if db_member == 0:
            raise HTTPException(status_code=400, detail="Delete failure")
    except:  # 삭제 중 문제 발생 시 400 error 발생
        raise HTTPException(status_code=400, detail="Delete failure")

    return db_member


@ router.get("/emotion/{member_uuid}", summary="특정 고객의 마지막 만족도 검사 결과 제공")
async def read_emotion(member_uuid: int):
    # uuid 기반으로 만족도 결과 가져오기
    db_emotion = crud.get_emotion(session, member_uuid)
    return db_emotion


@ router.post("/emotion", summary="만족도 검사 결과 저장 및 퇴장 시간 기록")
async def create_emotion(emotion: Emotion):
    # 감정 데이터 생성
    db_emotion = crud.create_emotion(session, emotion)
    if db_emotion is None:
        raise HTTPException(status_code=400, detail="Creation failure")

    # 나가는 시간 기록
    db_visited = visited_crud.get_visited_by_uuid(session, emotion.uuid)
    visited_crud.update_visited(session, db_visited, emotion.end_visit)

    return db_emotion
