import cv2
import numpy as np
import face_recognition

# 이미지 로드
imgElon = face_recognition.load_image_file('ImageBasic/musk1.jfif')
imgElon = cv2.cvtColor(imgElon, cv2.COLOR_BGR2RGB)

imgElon_test = face_recognition.load_image_file('ImageBasic/musk2.jfif')
imgElon_test = cv2.cvtColor(imgElon_test, cv2.COLOR_BGR2RGB)

imgIU = face_recognition.load_image_file('ImageBasic/IU1.jfif')
imgIU = cv2.cvtColor(imgIU, cv2.COLOR_BGR2RGB)

# 이미지 분석
# 일론 머스크
faceLoc = face_recognition.face_locations(imgElon)[0]
encodeElon = face_recognition.face_encodings(imgElon)[0]
cv2.rectangle(imgElon, (faceLoc[3], faceLoc[0]),
              (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

# 일론 머스크 테스트
faceLocTest = face_recognition.face_locations(imgElon_test)[0]
encodeElonTest = face_recognition.face_encodings(imgElon_test)[0]
cv2.rectangle(imgElon_test, (faceLocTest[3], faceLocTest[0]),
              (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

# 아이유
faceLocIU = face_recognition.face_locations(imgIU)[0]
encodeIU = face_recognition.face_encodings(imgIU)[0]
cv2.rectangle(imgIU, (faceLocIU[3], faceLocIU[0]),
              (faceLocIU[1], faceLocIU[2]), (255, 0, 255), 2)

# 일치 결과 비교
result1 = face_recognition.compare_faces([encodeElon], encodeElonTest)
result2 = face_recognition.compare_faces([encodeElon], encodeIU)
print('일론 + 일론 테스트 : ', result1)
print('일론 + IU 테스트 : ', result2)

# 이미지 출력
cv2.imshow('Elon Musk', imgElon)
cv2.imshow('Elon Musk Test', imgElon_test)
cv2.imshow('IU', imgIU)
cv2.waitKey(0)
