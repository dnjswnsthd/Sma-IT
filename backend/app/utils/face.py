import cv2
import numpy as np
import face_recognition
from models.model import MemberTable as Member

def face_check(img_path: str, members: Member):
    
    # 비교할 이미지 로드
    img_path = "./cam_img/" + img_path
    img = face_recognition.load_image_file(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #비교할 이미지 분석
    #print("타입 분석 : ",type(face_recognition.face_locations(img)), " 사이즈 : ", len(face_recognition.face_locations(img)))
    if len(face_recognition.face_locations(img)) == 0:
      return "얼굴인식 실패"

    # faceLoc = face_recognition.face_locations(img)[0]
    user = face_recognition.face_encodings(img)[0]
    # cv2.rectangle(img, (faceLoc[3], faceLoc[0]),
    #           (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

    #print(user)
    # 이미지 분석후 얼굴의 결과가 없으면 "얼굴인식이 안됬습니다" 리턴

    for member in members:
        #print(member.image)
        # 디비에 데이터를 가져와야함(임시 데이터 준형이 마스크얼굴)
        memberimg_path = "./member_img/" + member.image
        memberimg = face_recognition.load_image_file(memberimg_path)
        memberimg = cv2.cvtColor(memberimg, cv2.COLOR_BGR2RGB)

        #기존 이용자 얼굴 분석
        # memberfaceLoc = face_recognition.face_locations(memberimg)[0]
        memberface = face_recognition.face_encodings(memberimg)[0]
        # cv2.rectangle(memberimg, (memberfaceLoc[3], memberfaceLoc[0]),
        #       (memberfaceLoc[1], memberfaceLoc[2]), (255, 0, 255), 2)

        # 얼굴 비교 
        result = face_recognition.compare_faces([memberface], user)
        #print('준형이 + 사용자 : ', result)

        # 얼굴이 같으면 바로 리턴 하고 맴버정보 제공
        if result[0]:
            # cv2.imshow('cam', img)
            # cv2.imshow('member', memberimg)
            # cv2.waitKey(0)
            return member

    return "등록된 회원이 아닙니다"
   
 