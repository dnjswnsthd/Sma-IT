from sqlalchemy.orm import Session
from sqlalchemy import desc

from models.member import MemberTable, Member
from models.emotion import EmotionTable, Emotion
from models.visited import VisitedTable, Visited


def get_visiteds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VisitedTable).offset(skip).limit(limit).all()


def get_visited_by_uuid(db: Session, uuid: int):
    return db.query(VisitedTable).filter(VisitedTable.uuid == uuid).order_by(VisitedTable.visited_id.desc()).first()


def get_visited_by_uuid_all(db: Session, uuid: int):
    return db.query(VisitedTable).filter(VisitedTable.uuid == uuid).order_by(VisitedTable.visited_id.asc()).all()


def create_visited(db: Session, uuid: int, start_visit: str):
    db_visited = VisitedTable()
    db_visited.uuid = uuid
    db_visited.start_visit = start_visit
    db_visited.end_visit = '1111-11-11 11:11:11'

    try:
        db.add(db_visited)
        db.commit()
        db.refresh(db_visited)
    except:
        db.rollback()
        raise

    return None


def update_visited(db: Session, db_visited: VisitedTable, end_visited: str):
    db_visited.end_visit = end_visited

    try:
        db.commit()
        db.refresh(db_visited)
    except:
        db.rollback()
        raise

    return db_visited


def delete_visited_by_uuid(db: Session, uuid: int):
    db_member = VisitedTable()

    try:
        db_member = db.query(VisitedTable).filter(
            MemberTable.uuid == uuid).delete()
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise

    return db_member
