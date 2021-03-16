from sqlalchemy.orm import Session

from models import model

def get_members(db: Session):
    return db.query(model.MemberTable).all()

def get_member_by_name(db: Session, member_name: str):
    return db.query(model.MemberTable).filter(model.MemberTable.name == member_name).first()

def get_member_by_uuid(db: Session, member_uuid: int):
    return db.query(model.MemberTable).filter(model.MemberTable.uuid == member_uuid).first()

def create_member(db: Session, member: model.Member, time : str):
    db_member = model.MemberTable()
    db_member.name = member.name
    db_member.age = member.age
    db_member.interests = member.interests
    db_member.requirements = member.requirements
    db_member.join_date = time
    db_member.image = member.image

    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def delete_member_by_uuid(db: Session, member_uuid: int):
    db_member = model.MemberTable()
    db_member = db.query(model.MemberTable).filter(model.MemberTable.uuid == member_uuid).delete()
    db.commit()
    return db_member

def update_member(db: Session, db_member: model.MemberTable, member:model.Member):
    db_member.uuid = member.uuid
    db_member.name = member.name
    db_member.age = member.age
    db_member.interests = member.interests
    db_member.requirements = member.requirements
    db_member.image = member.image
    db.commit()
    return db_member