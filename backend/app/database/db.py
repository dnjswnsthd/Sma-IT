from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

user_name = "smait"
user_pwd = "1234"
db_host = "j4d102.p.ssafy.io:3306"
db_name = "smait"

DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    user_name,
    user_pwd,
    db_host,
    db_name
)

ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    echo=True
)

session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property() 