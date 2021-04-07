from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from models.member import MemberTable, Member, UpdateMember
from models.emotion import EmotionTable, Emotion
from models.visited import VisitedTable
from models.images import ImagesTable, Images

import os


# skip ~ limit 까지의 고객 정보 및 방문 시간, 퇴장 시간 가져오기
def get_members(db: Session, skip: int = 0, limit: int = 100):
    # 가장 최근 방문 시간을 가져오기 위한 Subquery 생성
    stmt = db.query(VisitedTable.uuid, func.max(VisitedTable.start_visit).label(
        'start_visit'), func.max(VisitedTable.end_visit).label('end_visit')).group_by(VisitedTable.uuid).subquery()

    members = []
    # member 테이블과 subquery의 join을 통한 고객 정보와 방문 시간, 퇴장 시간 가져오기
    for member, start_visit, end_visit in db.query(MemberTable, stmt.c.start_visit, stmt.c.end_visit).join(
            stmt, MemberTable.uuid == stmt.c.uuid).order_by(MemberTable.uuid).offset(skip).limit(limit):
        # 결과를 json형식으로 제공하기 위하여 dict 형으로 만들어 줌
        mem = {
            'uuid': member.uuid,
            'name': member.name,
            'age': member.age,
            'interests': member.interests,
            'requirements': member.requirements,
            'join_date': member.join_date,
            'image': member.image,
            'start_visit': str(start_visit),
            'end_visit': str(end_visit),
        }
        members.append(mem)

    return members


# 고객 이름을 기반으로 고객 정보 가져오기
def get_member_by_name(db: Session, member_name: str):
    return db.query(MemberTable).filter(MemberTable.name == member_name).first()


# uuid를 기반으로 고객 정보 가져오기
def get_member_by_uuid(db: Session, member_uuid: int):
    return db.query(MemberTable).filter(MemberTable.uuid == member_uuid).first()


# 등록된 사진 이름으로 고객 정보 가져오기
def get_member_by_image(db: Session, member_img: int):
    return db.query(MemberTable).filter(MemberTable.image == member_img).first()


# 고객 정보 등록
def create_member(db: Session, member: Member, time: str):
    # 등록을 위한 고객 정보 기록
    db_member = MemberTable()
    db_member.name = member.name
    db_member.age = member.age
    db_member.interests = member.interests
    db_member.requirements = member.requirements
    db_member.join_date = time
    db_member.image = member.image

    try:
        # 고객 정보 등록
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
    except:
        # 문제 발생 시 rollback
        db.rollback()
        raise SQLAlchemyError

    return db_member


# 고객이 등록한 이미지 이름을 DB에 저장
def update_image_member(db: Session, db_member: MemberTable, image: int):
    try:
        db_member.image = str(image) + ".jpg"
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise SQLAlchemyError
    return db_member


# uuid 기반으로 고객 정보 삭제
def delete_member_by_uuid(db: Session, member_uuid: int):
    try:
        db_member = db.query(MemberTable).filter(
            MemberTable.uuid == member_uuid).delete()

        path = "../img/member_img/"+str(member_uuid)+".jpg"
        if os.path.isfile(path):
            os.remove(path)
        db.commit()
    except:
        db.rollback()
        raise SQLAlchemyError
    return db_member


# 고객 정보 수정
def update_member(db: Session, db_member: MemberTable, member: UpdateMember):
    try:
        db_member.uuid = member.uuid
        db_member.name = member.name
        db_member.age = member.age
        db_member.interests = member.interests
        db_member.requirements = member.requirements
        db_member.image = member.image
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise
    return db_member


# parameter : uuid 의 emotion 값 list로 return
def get_emotion(db: Session, member_uuid: int):
    return db.query(EmotionTable).filter(member_uuid == EmotionTable.uuid).all()


# Insert Emotion
def create_emotion(db: Session, emotion: Emotion):
    db_emotion = EmotionTable()
    db_emotion.uuid = emotion.uuid
    db_emotion.anger = emotion.anger
    db_emotion.contempt = emotion.contempt
    db_emotion.disgust = emotion.disgust
    db_emotion.fear = emotion.fear
    db_emotion.happiness = emotion.happiness
    db_emotion.neutral = emotion.neutral
    db_emotion.sadness = emotion.sadness
    db_emotion.surprise = emotion.surprise
    db_emotion.end_visit = emotion.end_visit
    try:
        db.add(db_emotion)
        db.commit()
        db.refresh(db_emotion)
    except:
        db.rollback()
        raise SQLAlchemyError
    return db_emotion

def get_images(db: Session):
    return db.query(Images).all()

def create_images(db: Session, member_uuid: int, image_bytes: str):
    db_images = ImagesTable()
    db_images.member_uuid = member_uuid
    db_images.image = image_bytes

    try:
        db.add(db_images)
        db.commit()
        db.refresh(db_images)
    except:
        db.rollback()
        raise SQLAlchemyError
    return db_images
   