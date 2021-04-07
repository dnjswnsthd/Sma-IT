from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from models.member import MemberTable, Member, UpdateMember
from models.emotion import EmotionTable, Emotion
from models.visited import VisitedTable
from models.images import ImagesTable, Images

import os


def get_members(db: Session, skip: int = 0, limit: int = 100):
    stmt = db.query(VisitedTable.uuid, func.max(VisitedTable.start_visit).label(
        'start_visit'), func.max(VisitedTable.end_visit).label('end_visit')).group_by(VisitedTable.uuid).subquery()
    # temp, start_visit, end_visit = db.query(MemberTable, stmt.c.start_visit, stmt.c.end_visit.label('end_visit')).join(
    #     stmt, MemberTable.uuid == stmt.c.uuid).order_by(MemberTable.uuid).offset(skip).limit(limit).all()
    members = []
    for member, start_visit, end_visit in db.query(MemberTable, stmt.c.start_visit, stmt.c.end_visit).join(
            stmt, MemberTable.uuid == stmt.c.uuid).order_by(MemberTable.uuid).offset(skip).limit(limit):
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

    # return db.query(MemberTable).order_by(MemberTable.uuid).offset(skip).limit(limit).all()
    return members


def get_member_by_name(db: Session, member_name: str):
    return db.query(MemberTable).filter(MemberTable.name == member_name).first()


def get_member_by_uuid(db: Session, member_uuid: int):
    return db.query(MemberTable).filter(MemberTable.uuid == member_uuid).first()


def get_member_by_image(db: Session, member_img: int):
    return db.query(MemberTable).filter(MemberTable.image == member_img).first()


def create_member(db: Session, member: Member, time: str):
    db_member = MemberTable()
    db_member.name = member.name
    db_member.age = member.age
    db_member.interests = member.interests
    db_member.requirements = member.requirements
    db_member.join_date = time
    db_member.image = member.image

    try:
        db.add(db_member)
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise SQLAlchemyError

    return db_member


def update_image_member(db: Session, db_member: MemberTable, image: int):
    try:
        db_member.image = str(image) + ".jpg"
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise SQLAlchemyError
    return db_member


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
   