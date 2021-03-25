import os
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import paddlehub as hub

def mask_check(img_path: str):
    # 사진 경로
    img_path = "../cam_img/" + img_path
    test_img_path = [img_path]
    img = mpimg.imread(test_img_path[0])


    hub.server_check()

    # 얼굴인식 및 마스크인식 모듈
    module = hub.Module(name="pyramidbox_lite_mobile_mask")

    imgs = [cv2.imread(test_img_path[0])]

    # 얼굴인식 및 마스크 인식
    results = module.face_detection(images=imgs, use_multi_scale=True, shrink=0.6, visualization=True, output_dir='detection_result')

    for result in results:
        print(result)
    
    return results
    