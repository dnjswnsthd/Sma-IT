from typing import List
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import datetime

from database.db import session
from database.model import Member, MemberTable

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
    members = session.query(MemberTable).all()

    return members


@app.get("/members/{member_uuid}")
async def read_member(member_uuid: int):
    member = session.query(MemberTable).filter(MemberTable.uuid == member_uuid).first()

    return member


@app.post("/members")
async def create_members(member: Member):
    now = datetime.datetime.now()

    memberT = MemberTable()
    memberT.uuid = member.uuid
    memberT.name = member.name
    memberT.age = member.age
    memberT.interests = member.interests
    memberT.requirements = member.requirements
    memberT.join_date = now.strftime('%Y-%m-%d %H:%M:%S')
    memberT.image = member.image

    session.add(memberT)
    session.commit()

    return f"{member.name} created..."

@app.put("/members")
async def update_members(members: List[Member]):
    for i in members:
        member = session.query(MemberTable).filter(MemberTable.uuid == i.uuid).first()
        member.uuid = i.uuid
        member.name = i.name
        member.age = i.age
        member.interests = i.interests
        member.requirements = i.requirements
        member.join_date = i.join_date
        member.image = i.image

    return f"{member.name} updated..."

@app.delete("/members")
async def delete_members(member_uuid: int):
    member = session.query(MemberTable).filter(MemberTable.uuid == member_uuid).delete()
    session.commit()

    return member