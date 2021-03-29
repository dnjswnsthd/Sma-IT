from fastapi import APIRouter, File, Form, UploadFile
from models.model import Member, Emotion

from crud import member_crud as crud
from database.db import session

import datetime

router = APIRouter()


@router.get("/")
async def read_members_limit(start: int = 0, limit: int = 10):
    members = crud.get_members(session, start, limit)

    return members


@router.get("/{member_uuid}")
async def read_member(member_uuid: int):
    member = crud.get_member_by_uuid(session, member_uuid)
    return member


@router.post("/")
async def create_members(member: Member, file: UploadFile = File(...)):
    # 중복체크인 나중에 따로 db에 데이터 추가해서 걸러야할듯
    db_member = crud.get_member_by_name(session, member.name)
    # 이미 가입된 회원
    if db_member:
         raise HTTPException(status_code=400, detail="?? already registered")
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_member = crud.create_member(session, member, now)
    # 가입 실패
    if db_member is None:
        raise HTTPException(status_code=400, detail="Creation failure")
    else:
        content = await file.read()
        with open(f'../img/member_img/{db_member.image}', 'wb') as fh:
        fh.write(content)

    return db_member


@router.put("/")
async def update_members(member: Member):
    db_member = crud.get_member_by_name(session, member.name)
    if db_member is None:
        raise HTTPException(status_code=400, detail="No members")
    db_member = crud.update_member(session, db_member, member)
    print(db_member)
    return db_member


@router.delete("/")
async def delete_members(member_uuid: int):
    db_member = crud.delete_member_by_uuid(session,member_uuid)
    if db_member is None:
        raise HTTPException(status_code=400, detail="Delete failure")
    return db_member
@router.get("/emotion/{member_uuid}")
async def read_emotion(member_uuid: int):
    db_emotion = crud.get_emotion(session, member_uuid)
    return db_emotion

@router.post("/emotion")
async def create_emotion(emotion: Emotion,):
    db_emotion = crud.create_emotion(session, emotion)
    if db_emotion is None:
        raise HTTPException(status_code=400, detail="Creation failure")

    return db_emotion