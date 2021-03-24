from fastapi import APIRouter

from models.model import Member
from crud import member_crud as crud
from database.db import session

import numpy as np

from utils.mask import mask_check
from utils.face import face_check

router = APIRouter()

@router.get("/{img_path:path}")
async def mask_checking(img_path: str):
    print(img_path)
    members = crud.get_members(session)
    face_compare = face_check(img_path, members)
    return face_compare



@router.get("/mask/{img_path:path}")
async def mask_checking(img_path: str):
    print(img_path)
    mask_data = mask_check(img_path)
    return mask_data
