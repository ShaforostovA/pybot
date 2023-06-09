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
    name = Column(String)

class Department(DeclBase):
    __tablename__ = "departments"
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    owner = Column(String)

class DepartmentRole(DeclBase):
    __tablename__ = "department_roles"
    department_id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, primary_key=True)

class NoteType(DeclBase):
    __tablename__ = "note_types"
    id = Column(BigInteger, primary_key=True)
    name = Column(String)

class NoteStatus(DeclBase):
    __tablename__ = "note_statuses"
    id = Column(BigInteger, primary_key=True)
    name = Column(String)

class Note(DeclBase):
    __tablename__ = "notes"
    id = Column(BigInteger, primary_key=True)
    title = Column(String)
    description = Column(String)
    owner = Column(String)
    type = Column(BigInteger)
    status = Column(BigInteger)
    recipient = Column(String)
    date_start = Column(DateTime)
    date_end = Column(DateTime)
    date_create = Column(DateTime, default=datetime.datetime.utcnow())
    date_update = Column(DateTime, default=datetime.datetime.utcnow())

if __name__=='__main__':
    from settings import DB_PATH

    engine = create_engine(DB_PATH)

    SessionClass = sessionmaker(bind=engine)
    db_session = SessionClass()

    DeclBase.metadata.create_all(engine)

    db_session.commit()