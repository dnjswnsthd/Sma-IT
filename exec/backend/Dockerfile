FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY ./app /app

RUN pip install --upgrade pip
RUN pip install pip cmake numpy opencv-python-headless pillow

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install dlib
RUN pip install face_recognition

RUN pip install pymysql sqlalchemy python-multipart
RUN pip install async-exit-stack async-generator
RUN pip install tensorflow

EXPOSE 8000