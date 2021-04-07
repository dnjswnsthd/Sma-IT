import cv2
import face_recognition

import os

from models.images import Images, ImagesTable

from crud import member_crud as crud
from database.db import session

import numpy as np

def face_check(img_path: str):
    # 비교할 이미지 로드
    img_path = "../img/cam_img/" + img_path
    img = face_recognition.load_image_file(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if len(face_recognition.face_locations(img)) == 0:
        return "얼굴인식 실패"

    user = face_recognition.face_encodings(img)[0]
    
    members = crud.get_images(session)

    uuid_img = None
    max = 0

    for member in members:
        # 얼굴 비교
        result = face_recognition.compare_faces([np.fromstring(member.image)], user)
        faceDist = face_recognition.face_distance([np.fromstring(member.image)], user)

        # 얼굴이 같으면 바로 리턴 하고 맴버정보 제공
        if result[0]:
            if max < 1 - faceDist:           
                uuid_img = str(member.member_uuid) + ".jpg"
                max = 1 - faceDist

    if uuid_img == None:
        return "등록된 회원이 아닙니다"

    return uuid_img

def face_image(image: str):
    memberimg_path = "../img/member_img/" + image
    memberimg = face_recognition.load_image_file(memberimg_path)
    memberimg = cv2.cvtColor(memberimg, cv2.COLOR_BGR2RGB)

    memberface = face_recognition.face_encodings(memberimg)[0]

    member_uuid = int(image.split('.')[0])
    image_bytes = memberface.tostring()
    result = crud.create_images(session, member_uuid, image_bytes)

    return "OK"
    