import cv2
import face_recognition

import os


def face_check(img_path: str):
    # 비교할 이미지 로드
    img_path = "../img/cam_img/" + img_path
    img = face_recognition.load_image_file(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    if len(face_recognition.face_locations(img)) == 0:
        return "얼굴인식 실패"

    user = face_recognition.face_encodings(img)[0]
    members = os.listdir('../img/member_img')

    uuid_img = None
    max = 0

    for member in members:
        # 디비에 데이터를 가져와야함(임시 데이터 준형이 마스크얼굴)
        memberimg_path = "../img/member_img/" + member
        memberimg = face_recognition.load_image_file(memberimg_path)
        memberimg = cv2.cvtColor(memberimg, cv2.COLOR_BGR2RGB)

        # 기존 이용자 얼굴 분석
        memberface = face_recognition.face_encodings(memberimg)[0]

        # 얼굴 비교
        result = face_recognition.compare_faces([memberface], user)
        faceDist = face_recognition.face_distance([memberface], user)
        print(f'{member} + {img_path} test : {1 - faceDist}')
        print(result[0])
        print('---------------------')

        # 얼굴이 같으면 바로 리턴 하고 맴버정보 제공
        if result[0]:
            if max < 1 - faceDist:
                uuid_img = member
                max = 1 - faceDist

    if uuid_img == None:
        return "등록된 회원이 아닙니다"

    return uuid_img
