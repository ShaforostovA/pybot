from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime, BigInteger, SmallInteger, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
import datetime, json, random

DeclBase = declarative_base()

class Role(DeclBase):
    __tablename__ = "roles"
    id = Column(BigInteger, primary_key=True)
    name = (Column, String)

class User(DeclBase):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True)
    login = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    lastname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    date_create = Column(DateTime, default=datetime.datetime.utcnow())
    date_update = Column(DateTime, default=datetime.datetime.utcnow())

class UserRole(DeclBase):
    __tablename__ = "user_roles"
    user_id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, primary_key=True)

class Department(DeclBase):
    __tablename__ = "departments"
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    owner_id = Column(BigInteger)

class DepartmentRole(DeclBase):
    __tablename__ = "department_roles"
    department_id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, primary_key=True)

class NodeType(DeclBase):
    __tablename__ = "note_types"
    id = Column(BigInteger, primary_key=True)
    name = (Column, String)

class NodeStatus(DeclBase):
    __tablename__ = "note_statuses"
    id = Column(BigInteger, primary_key=True)
    name = (Column, String)

class Note(DeclBase):
    __tablename__ = "notes"
    id = Column(BigInteger, primary_key=True)
    tile = (Column, String)
    description = (Column, String)
    owner_id = Column(BigInteger)
    type = Column(BigInteger)
    status = Column(BigInteger)
    recipient = Column(BigInteger)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    date_create = Column(DateTime, default=datetime.datetime.utcnow())
    date_update = Column(DateTime, default=datetime.datetime.utcnow())

class Session(DeclBase):
    __tablename__ = "sessions"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    isLogout = Column(Boolean, default=True)
    date_start = Column(DateTime, default=datetime.datetime.utcnow())
    date_end = Column(DateTime)

if __name__=='__main__':
    from settings import DB_PATH

    engine = create_engine(DB_PATH)

    SessionClass = sessionmaker(bind=engine)
    db_session = SessionClass()

    DeclBase.metadata.create_all(engine)

    db_session.commit()