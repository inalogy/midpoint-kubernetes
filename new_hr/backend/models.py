import os
import time

from sqlalchemy import (Column, Date, ForeignKey, Integer, LargeBinary, String,
                        create_engine)
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy_utils import create_database, database_exists

### DB MODELS
Base = declarative_base()
class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    position_id = Column(Integer, ForeignKey('positions.id'))
    first_name = Column(String)
    last_name = Column(String)
    display_name = Column(String)
    sex = Column(String)
    birthdate = Column(Date)
    id_card = Column(String)
    personal_email = Column(String)
    personal_phone = Column(String)
    iban = Column(String)
    home_street = Column(String)
    home_city = Column(String)
    home_postal_code = Column(String)
    home_country = Column(String)
    work_street = Column(String)
    work_city = Column(String)
    work_postal_code = Column(String)
    work_country = Column(String)
    language = Column(String)
    nationality = Column(String)
    employment_type = Column(String)
    division = Column(String)
    picture = Column(LargeBinary, nullable=True)

    department = relationship("Department", back_populates="employees")
    position = relationship("Position", back_populates="employees")

Department.employees = relationship("Employee", order_by=Employee.id, back_populates="department")
Position.employees = relationship("Employee", order_by=Employee.id, back_populates="position")

# DATABASE SETTINGS
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@" \
                f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

def init_database_if_not_exists():
    max_retries = 30
    timeout = 6
    retries = 0

    while retries < max_retries:
        try:
            print("Trying to create database....")
            if not database_exists(engine.url):
                create_database(engine.url, encoding="utf8")
            engine.connect()
            return True
        except OperationalError:
            print(f"Operational Error, sleeping for `{timeout}` seconds.")
            time.sleep(timeout)
            retries += 1
    raise DatabaseError(
        f"Database is not ready within {timeout*retries} seconds.")

init_database_if_not_exists()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(engine)