from fastapi import APIRouter, File, UploadFile

from models.member import Member
from crud import member_crud as crud
from database.db import session

import numpy as np
import base64

import cv2

from utils.mask import mask_check
from utils.face import face_check

router = APIRouter()


@router.post("/")
async def mask_checking(file: UploadFile = File(...)):
    members = crud.get_members(session)
    content = await file.read()
    with open(f'../img/cam_img/{file.filename}', 'wb') as fh:
        fh.write(content)
    face_data = face_check(file.filename, members)
    # mask_data = mask_check()
    return face_data

@router.get("/test/{img_path:path}")
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
