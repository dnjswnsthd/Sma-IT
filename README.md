<img src="C:\Users\multicampus\Desktop\ㄴㅁㅇㄹ.png" alt="ㄴㅁㅇㄹ" style="width:200px; height:150px; float : left; display : block;" />

 ![Generic badge](https://img.shields.io/badge/Vue.js-2.6.1-orange.svg) ![Generic badge](https://img.shields.io/badge/python-3.8.0-{color}.svg) ![Generic badge](https://img.shields.io/badge/Axios-0.21.1-blue.svg)![Generic badge](https://img.shields.io/badge/Uvicorn-fe0094.svg)![Generic badge](https://img.shields.io/badge/FastAPI-red.svg)![Generic badge](https://img.shields.io/badge/Nginx-lightgrey.svg)![Generic badge](https://img.shields.io/badge/Mysql-yellowgreen.svg)

# Sma-IT

## '얼굴 인식을 통한 효율적 마케팅 실현 서비스'

프로젝트 명은 'Sma-IT'로 'Smart Marketing With IT' 라는 뜻을 갖고 있으며,

한글 뜻으론 "강타하다"라는 뜻으로, 고객님의 마음을 강타하는 마켓팅을 하자라는

함축적 의미를 담고있습니다.

# 기획 배경

매장 방문시 발생할 수 있는 이슈에서 얼굴 인식만을 통해

고객의 관심사나 요구사항 등을 직원이 미리 알고 취향저격 서비스를 제공할 수 있으며,

얼굴 인식을 통한 간편 결제 및 감정 분석을 통한 만족도 검사가 가능합니다.

즉 얼굴만 들고 다닌다면, 모든 이슈에 대응할 수 있는 편리한 매장을

구현하고자 기획하게 되었습니다.

# Smait 기능 소개

### Mask 착용 체크

- 코로나 19로 인한 고객님들의 방역에 대한 불안감을 덜어드리기 위해서

  ```
  매장 방문시 입장때 얼굴 인식을 통한 마스크 착용 여부를 확인하여 
  ```

→ 마스크를 착용했을 경우에는 입장 가능

→ 마스크를 미착용했을 경우에는 입장이 불가능하다는 안내를 하게 됩니다.

### 방문 고객 정보 캡셔닝

- 마스크 착용에 대한 판단이 마친 후, 마스크를 착용한 고객님께서

  매장에 등록된 고객님이시라면, 고객님의 정보를 매장 직원용 Page를 통해서

볼 수 있어, 응대에 앞서 고객님의 관심사 및 요구사항을 알 수 있습니다.

### 얼굴 인식 결제

- 매장에 방문 했을 때, 지갑 또는 핸드폰을 두고 와서

  결제를 못하고 돌아가시는 경우를 방지하고자, 얼굴 인식을 통해서

  등록해놓은 결제 시스템으로 간편 결제를 할 수 있습니다.

### 감정 분석을 통한 만족도 기록

- 매장을 떠나실 때, 만족도 평가를 남기고 싶지만,

  많은 항목의 설문조사는 번거로워 하지 않는 경우가 많기 때문에,

  이런 상황을 방지하기 위해, 얼굴 인식을 통한 감정 분석을 통해

  만족도를 기록할 수 있습니다.

# Installation

## Frontend

```bash
cd frontend
npm install
npm run serve
```

Microsoft Azure FaceAPI Key & EndPoint 생성 필요

## Backend

```bash
cd backend
cd app
uvicorn main:app --reload
```

## AI 특화 개발 환경 설정

### Anaconda

------

### 가상 환경 생성 및 활성화

```bash
conda create -n <project-name> python=<version>
conda activate <project-name>
```

### 필요 라이브러리 설치

```bash
conda install <librarys>
```

### Anaconda 기본 명령어

```bash
# 가상환경 리스트 조회
conda env list

# 가상환경 생성
conda create -n <가상환경 이름>
# 특정 버전의 파이썬을 사용하고 싶을 때
conda create -n <가상환경 이름> python=<version>

# 가상환경 복제
conda create --clone <복제할 가상환견 이름> -n <새 가상환경 이름>

# 가상환경 활성화/비활성화
conda activate <가상환경 이름>
conda deactivate

# 가상환경 삭제
conda env remove -n <가상환경 이름>

# 설치된 아나콘다 정보 조회
conda info

# 가상환경에 설치된 패키지 리스트 조회
conda list

# 패키지 설치
conda install <패키지 이름>
# 현재 활성화된 환경이 아닌 다른 환경에 설치할 경우
conda install -n <가상환경 이름> <패키지 이름>

# 설치된 패키지 업데이트
conda update <패키지 이름>

# 설치된 패키지 삭제
conda remove -n <가상환경 이름> <패키지 이름>
```

## Backend modules 패키지

### face_recognition 에서 사용하는 패키지

```bash
conda create -n <가상환경 이름> python=3.8
conda activate <가상환경 이름>

conda install pip cmake numpy
conda install opencv

conda install pillow
conda install -c conda-forge dlib
conda install -c akode face_recognition_models
pip install --no-dependencies face_recognition
```

### face_test 에서 사용하는 패키지

```bash
conda create -n <가상환경 이름> python=3.8  #3.6이상
conda activate <가상환경 이름>

python -m pip install paddlepaddle==2.0.1 -i <https://mirror.baidu.com/pypi/simple>
pip install paddlehub==2.0.0rc0

python face_test.py # <-- 실행

# <https://github.com/paddlepaddle/paddlehub> 
pip install pymysql
pip install sqlalchemy
pip install async-exit-stack async-generator
```

# 배포

## Docker & Jenkins

- Docker에 Jenkins image를 만들고 Jenkinxs와 git commit 시 자동으로 업데이트 반영 되도록 배포
- Frontend와 Backend에 각각 Dockerfile을 생성해 배포 설저을 저장

### Nginx & SSL

- HA와 Load Balancing을 위하여 Nginx 적용
- SSL 키를 적용하여 https 준수

# 프로젝트 상세 소개

### 고객 입장 얼굴 인식 페이지

<div>
    <img src="C:\Users\multicampus\Desktop\Untitled.png" style="width: 50%; height : 500px; float:left; display : block;" />
    <img src="C:\Users\multicampus\Desktop\Untitled (1).png" style="width: 50%;height : 500px;float: right ; display : block;" />
</div>



























- 얼굴 인식을 통한 마스크 착용 여부를 판단
- 얼굴 인식을 통한 등록된 고객 여부 판단

—-—-—-—-—-—-—-—-—-—-—-—-—-—개발 진행중—-—-—-—-—-—-—-—-—-—-—————

# ER-Diagram

<img src="C:\Users\multicampus\Desktop\erd.png"  />

# 기술스택

<img src="C:\Users\multicampus\Desktop\stack.png" style="zoom: 80%;" />

# 진행프로세스

<img src="C:\Users\multicampus\Desktop\ing.png" style="zoom:67%; " />





# 팀 구성원 소개 및 역할



<img src="C:\Users\multicampus\Desktop\23242.png" style="zoom:67%;" />