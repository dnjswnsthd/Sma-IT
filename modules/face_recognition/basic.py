import cv2
import numpy as np
import face_recognition
import os

# 설정
path = 'ImageBasic'
images = []
classNames = []
myList = os.listdir(path)

# 사진 디렉토리 내 이미지 경로 리스트 추출
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


# 각 사진별 인코딩 함수
def find_encodings(image_paths):
    encode_list = []

    for image_path in image_paths:
        inner_image = cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(inner_image)[0]
        encode_list.append(encode)
    return encode_list


# 인코딩 리스트 받기
encodeListKnown = find_encodings(images)
print(f'Encoding Complete {len(encodeListKnown)}')

# 캠 영상 받아서 처리
cap = cv2.VideoCapture(0)

while True:
    success, cap_img = cap.read()
    imgS = cv2.resize(cap_img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # 캠 얼굴 인코딩
    faceCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # 캠 얼굴과 메모리상 인코딩 데이터간의 비교
    for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(cap_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(cap_img, (x1, y2 - 35), (x2, y2),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(cap_img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('cam', cap_img)
    cv2.waitKey(1)
