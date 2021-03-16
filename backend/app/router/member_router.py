from fastapi import APIRouter
from models.model import Member

from crud import member_crud as crud
from database.db import session

router = APIRouter()


@router.get("/")
async def read_members():
    members = crud.get_members(session)
    return members


@router.get("/{member_uuid}")
async def read_member(member_uuid: int):
    member = crud.get_member_by_uuid(session, member_uuid)
    return member


@router.post("/")
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