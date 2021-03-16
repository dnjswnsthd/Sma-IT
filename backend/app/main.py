from typing import List
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

import datetime

from database.db import session
from models.model import Member, MemberTable
from crud import member_crud as crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/members")
async def read_members():
    members = crud.get_members(session)
    return members


@app.get("/members/{member_uuid}")
async def read_member(member_uuid: int):
    member = crud.get_member_by_uuid(session, member_uuid)
    return member


@app.post("/members")
async def create_members(member: Member):
    # 중복체크인 나중에 따로 db에 데이터 추가해서 걸러야할듯
    db_member = crud.get_member_by_name(session, member.name)
    if db_member:
         raise HTTPException(status_code=400, detail="?? already registered")
    
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db_member = crud.create_member(session, member, now)
    if db_member is None:
        raise HTTPException(status_code=400, detail="Creation failure")

    return db_member

@app.put("/members")
async def update_members(member: Member):
    db_member = crud.get_member_by_name(session, member.name)
    if db_member is None:
        raise HTTPException(status_code=400, detail="No members")
    db_member = crud.update_member(session, db_member, member)
    print(db_member)
    return db_member

@app.delete("/members")
async def delete_members(member_uuid: int):
    db_member = crud.delete_member_by_uuid(session,member_uuid)
    if db_member is None:
        raise HTTPException(status_code=400, detail="Delete failure")
    return db_member
    