from fastapi import APIRouter, File, UploadFile

from models.visited import Visited
from crud import member_crud, visited_crud

from database.db import session

import numpy as np
import base64

import cv2

from utils.mask import mask_check
from utils.face import face_check

router = APIRouter()


@router.post("/{start_visted}" , summary="얼굴 인식 및 마스크 인식")
async def face_mask_checking(start_visted: str, file: UploadFile = File(...)):
    # 회원정보 전체 조회
    members = member_crud.get_members(session)
    
    # 이미지 저장
    content = await file.read()
    with open(f'../img/cam_img/{file.filename}', 'wb') as fh:
        fh.write(content)
   
    #얼굴인식 및 마스크 인식
    face_data = face_mask_check(file.filename, members)

    # 입장 시간 저장
    visited_crud.create_visited(session, face_data["member"].uuid, start_visted)
    
    return face_data

@router.post("/onlyface", summary="얼굴인식")
async def face_checking(file: UploadFile = File(...)):
    # 회원정보 전체 조회
    members = member_crud.get_members(session)
    
    # 이미지 저장
    content = await file.read()
    with open(f'../img/cam_img/{file.filename}', 'wb') as fh:
        fh.write(content)
   
    #얼굴인식
    face_data = face_check(file.filename, members)

    return face_data

@router.get("/mask/{img_path:path}", summary="마스크 인식")
async def mask_checking(img_path: str):
    print(img_path)
    mask_data = mask_check(img_path)
    return mask_data

