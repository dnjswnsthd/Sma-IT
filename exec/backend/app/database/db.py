from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
# 데이터 베이스 정보 및 사용자 정보
user_name = "smait"
user_pwd = "1234"
db_host = "j4d102.p.ssafy.io:3306"
db_name = "smait"
# 데이터 베이스 연결을 위한 URL
DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_pwd,
    db_host,
    db_name
)
# engine 생성
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=False,
    poolclass=NullPool
)
# 싱글턴 패턴으로 DB 연결
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()
