from sqlalchemy.orm import Session

from models.member import MemberTable, Member
from models.emotion import EmotionTable, Emotion

def get_members(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MemberTable).offset(skip).limit(limit).all()

def get_member_by_name(db: Session, member_name: str):
    return db.query(MemberTable).filter(MemberTable.name == member_name).first()

def get_member_by_uuid(db: Session, member_uuid: int):
    return db.query(MemberTable).filter(MemberTable.uuid == member_uuid).first()

def create_member(db: Session, member: Member, time : str):
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
        raise

    return db_member

def update_image_member(db: Session, db_member: MemberTable, image: int):
    db_member.image = str(image) + ".jpg"
    try:
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise
    return db_member


def delete_member_by_uuid(db: Session, member_uuid: int):
    db_member = MemberTable()
    try:
        db_member = db.query(MemberTable).filter(MemberTable.uuid == member_uuid).delete()
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise
    return db_member

def update_member(db: Session, db_member: MemberTable, member: Member):
    db_member.uuid = member.uuid
    db_member.name = member.name
    db_member.age = member.age
    db_member.interests = member.interests
    db_member.requirements = member.requirements
    db_member.image = member.image
    try:
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
        raise
    return db_emotion