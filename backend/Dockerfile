FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY ./app /app

RUN pip install --upgrade pip

RUN pip install pip cmake numpy opencv-python-headless pillow
RUN pip install dlib
RUN pip install face_recognition
RUN python -m pip install paddlepaddle==2.0.1 -i https://mirror.baidu.com/pypi/simple
RUN pip install paddlehub==2.0.0rc0

RUN pip install pymysql sqlalchemy
RUN pip install async-exit-stack async-generator

EXPOSE 8000