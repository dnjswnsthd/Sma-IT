from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from models.member import MemberTable
from models.visited import VisitedTable


# 고객의 방문 정보 제공
def get_visiteds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(VisitedTable).offset(skip).limit(limit).all()


# uuid 기반으로 특정 고객의 최근 방문 정보 제공
def get_visited_by_uuid(db: Session, uuid: int):
    return db.query(VisitedTable).filter(VisitedTable.uuid == uuid).order_by(VisitedTable.visited_id.desc()).first()


# uuid 기반으로 특정 고객의 모든 방문 기록 제공
def get_visited_by_uuid_all(db: Session, uuid: int):
    return db.query(VisitedTable).filter(VisitedTable.uuid == uuid).order_by(VisitedTable.visited_id.asc()).all()


# 고객의 방문 정보 기록
def create_visited(db: Session, uuid: int, start_visit: str):
    db_visited = VisitedTable()
    db_visited.uuid = uuid
    db_visited.start_visit = start_visit
    db_visited.end_visit = start_visit

    try:
        db.add(db_visited)
        db.commit()
        db.refresh(db_visited)
    except:
        db.rollback()
        raise SQLAlchemyError

    return None


# 고객의 퇴장 시간 기록
def update_visited(db: Session, db_visited: VisitedTable, end_visited: str):
    db_visited.end_visit = end_visited

    try:
        db.commit()
        db.refresh(db_visited)
    except:
        db.rollback()
        raise SQLAlchemyError

    return db_visited


# 고객의 방문 기록 삭제
def delete_visited_by_uuid(db: Session, uuid: int):
    db_member = VisitedTable()

    try:
        db_member = db.query(VisitedTable).filter(
            MemberTable.uuid == uuid).delete()
        db.commit()
        db.refresh(db_member)
    except:
        db.rollback()
        raise SQLAlchemyError

    return db_member
