# python 3.6 이상
# python -m pip install paddlepaddle==2.0.1 -i https://mirror.baidu.com/pypi/simple
# pip install paddlehub==2.0.0rc0

import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import paddlehub as hub

# 사진 경로
test_img_path = ["./test.jpg"]
img = mpimg.imread(test_img_path[0])

# 사진 띄우기
# plt.figure(figsize=(10,10))
# plt.imshow(img)
# plt.axis('off')
# plt.show()

# 파일 오픈으로 경로 얻기
# with open('test.txt', 'r') as f:
#     test_img_path=[]
#     for line in f:
#         test_img_path.append(line.strip())
# print(test_img_path)

hub.server_check()

# 얼굴인식 및 마스크인식 모듈
module = hub.Module(name="pyramidbox_lite_mobile_mask")
# module = hub.Module(name="pyramidbox_lite_server_mask")

# 배경삭제 모듈
module2 = hub.Module(name="deeplabv3p_xception65_humanseg")

imgs = [cv2.imread(test_img_path[0])]

# 얼굴인식 및 마스크 인식
results = module.face_detection(images=imgs, use_multi_scale=True, shrink=0.6, visualization=True, output_dir='detection_result')

#배경 삭제
res = module2.segmentation(paths=["./test.jpg"], visualization=True, output_dir='humanseg_output')

# 얼굴인식 및 마스크 인식 결과
for result in results:
    print(result)

