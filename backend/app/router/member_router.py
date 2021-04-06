from fastapi import APIRouter, File, UploadFile, HTTPException

from models.member import Member, UpdateMember
from models.emotion import Emotion

from crud import member_crud as crud
from crud import visited_crud
from database.db import session

from sqlalchemy.exc import SQLAlchemyError

import base64
import datetime

router = APIRouter()


@router.get("/")
async def read_members_limit(start: int = 0, limit: int = 10):
    members = crud.get_members(session, start, limit)
    images = []
    for member in members:
        print(member)
        path = '../img/member_img/' + member['image']
        with open(path, 'rb') as img:
            base64_string = base64.b64encode(img.read())
            images.append(base64_string)
    data = dict(members=members, images=images)

    return data


@router.get("/{member_uuid}")
async def read_member(member_uuid: int):
    member = crud.get_member_by_uuid(session, member_uuid)
    return member


@router.post("/")
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
    except SQLAlchemyError:
        raise HTTPException(status_code=400, detail="Creation failure")

    db_member = crud.get_member_by_name(session, member.name)
    return db_member


@router.post("/image/{image}")
async def create_members_img(image: str, file: UploadFile = File(...)):
    content = await file.read()
    with open(f'../img/member_img/{image}', 'wb') as fh:
        fh.write(content)
    return "OK"


@router.put("/")
async def update_members(member: UpdateMember):
    db_member = crud.get_member_by_uuid(session, member.uuid)
    if db_member is None:
        raise HTTPException(status_code=400, detail="No members")
    db_member = crud.update_member(session, db_member, member)

    return db_member


@router.delete("/{member_uuid}")
async def delete_members(member_uuid: int):
    try:
        db_member = crud.delete_member_by_uuid(session, member_uuid)
        if db_member == 0:
            raise HTTPException(status_code=400, detail="Delete failure")
    except:
        raise HTTPException(status_code=400, detail="Delete failure")

    return db_member


@ router.get("/emotion/{member_uuid}")
async def read_emotion(member_uuid: int):
    db_emotion = crud.get_emotion(session, member_uuid)
    return db_emotion


@ router.post("/emotion")
async def create_emotion(emotion: Emotion):
    # 감정 데이터 생성
    db_emotion = crud.create_emotion(session, emotion)
    if db_emotion is None:
        raise HTTPException(status_code=400, detail="Creation failure")

    # 나가는 시간 기록
    db_visited = visited_crud.get_visited_by_uuid(session, emotion.uuid)
    visited_crud.update_visited(session, db_visited, emotion.end_visit)

    return db_emotion
