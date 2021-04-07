import cv2
import face_recognition

import os

from models.images import Images

from crud import member_crud as crud
from database.db import session

def face_check(img_path: str):
    # 비교할 이미지 로드
    img_path = "../img/cam_img/" + img_path
    img = face_recognition.load_image_file(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 이미지에서 얼굴을 인식하지 못한 경우
    if len(face_recognition.face_locations(img)) == 0:
        return "얼굴인식 실패"
    # 고객 이미지 encoding
    user = face_recognition.face_encodings(img)[0]
    # 저장 되어 있는 모든 이미지 정보 로딩
    members = os.listdir('../img/member_img')
    #members = crud.get_images(session)
    uuid_img = None
    max = 0
    # 등록된 모든 이미지와 받아온 얼굴을 비교하여 얼굴 인식 진행
    for member in members:
        # 등록되어 있는 이미지 로딩
        memberimg_path = "../img/member_img/" + member
        # 얼굴 비교를 위한 이미지 로드(흑백으로 바꾸어서 비교)
        memberimg = face_recognition.load_image_file(memberimg_path)
        memberimg = cv2.cvtColor(memberimg, cv2.COLOR_BGR2RGB)
        # 기존 이용자 얼굴 분석
        memberface = face_recognition.face_encodings(memberimg)[0]

        # 데이터 추가용
        member_uuid = int(member.split('.')[0])
        image_bytes = memberface.tostring()
        crud.create_images(session,member_uuid,image_bytes)

        # 얼굴 비교
        result = face_recognition.compare_faces([memberface], user)
        # 얼굴의 유사도 판별을 위한 dist 생성
        faceDist = face_recognition.face_distance([memberface], user)
        # 얼굴이 같다고 판단된 멤버들 중 유사도가 가장 높은 이미지를 리턴
        if result[0]:
            if max < 1 - faceDist:
                uuid_img = member
                max = 1 - faceDist
    # 선택된 이미지가 없다면 등록된 회원이 아님
    if uuid_img == None:
        return "등록된 회원이 아닙니다"

    return uuid_img

def face_image(image: str):
    memberimg_path = "../img/member_img/" + image
    memberimg = face_recognition.load_image_file(memberimg_path)
    memberimg = cv2.cvtColor(memberimg, cv2.COLOR_BGR2RGB)

    member_uuid = int(image.split('.')[0])
    image_bytes = memberface.tostring()
    result = crud.create_images(session, member_uuid, image_bytes)

    return "OK"
    