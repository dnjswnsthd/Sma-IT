from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException
from models.member import Member
from models.emotion import Emotion

from crud import member_crud as crud
from database.db import session

from typing import Optional

import datetime
from pydantic import BaseModel

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
async def create_members(member : Member):
    # 등록되있는지 체크
    db_member = crud.get_member_by_name(session, member.name)
    # 이미 가입된 회원
    if db_member:
         raise HTTPException(status_code=400, detail="?? already registered")
    
    # 시간생성
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 등록
    db_member = crud.create_member(session, member, now)
    # image 등록
    db_member = crud.update_image_member(session, db_member, db_member.uuid)
        
    # 가입 실패
    if db_member is None:
        raise HTTPException(status_code=400, detail="Creation failure")

    db_member = crud.get_member_by_name(session, member.name)
    return db_member

@router.post("/image/{image}")
async def create_members_img(image : str, file: UploadFile = File(...)): 
    content = await file.read()
    with open(f'../img/member_img/{image}', 'wb') as fh:
        fh.write(content)
    return "OK"

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