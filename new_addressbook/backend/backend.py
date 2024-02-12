""" Simple implementation of backend for addressbook """
import os
from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from sqlalchemy import (TIMESTAMP, Boolean, Column, Integer, MetaData, String,
                        Table, select)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# DATABASE SETTINGS
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# SECRET KEY FOR OAUTH
SECRET_KEY = os.getenv("SECRET_KEY", "MyHovercraftIsFullOfEels")
ALGORITHM = "HS256"

# Create async database engine
SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@" \
                          f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)  # Use AsyncSession


metadata = MetaData()
people = Table(
    "people",
    metadata,
    Column("first_name", String),
    Column("last_name", String),
    Column("tel_number", String),
    Column("fax_number", String),
    Column("office_id", Integer),
    Column("floor", Integer),
    Column("street_address", String),
    Column("city", String),
    Column("country", String),
    Column("postal_code", String),
    Column("validity", Boolean),
    Column("created", TIMESTAMP),
    Column("modified", TIMESTAMP),
    Column("username", String, primary_key=True),
    Column("password", String),
)
async def get_db():
    async with SessionLocal() as db:
        yield db

class People(BaseModel):
    first_name: str
    last_name: str
    tel_number: str
    fax_number: str
    office_id: int
    floor: int
    street_address: str
    city: str
    country: str
    postal_code: str
    validity: bool
    created: datetime
    modified: datetime
    username: str
    password: str

# Oauth scheme for password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Custom JSON scheme for validation
class OAuth2PasswordRequestJSON(BaseModel):
    username: str
    password: str


async def authenticate_user(username: str, password: str, db: AsyncSession):
    """ Authenticates user against the database """
    result = await db.execute(select(people).where(people.c.username == username))
    rows = result.fetchall()
    if rows and rows[0].password.strip() == password.strip():
        return rows[0]
    return False

def create_access_token(data: dict):
    """ Generates Access Token """
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """ Get user from the token """
    token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_name = token_data["username"]
    result = await db.execute(select(people).where(people.c.username == user_name))
    data = result.fetchall()
    if not data[0]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data[0]

# Login endpoint
@app.post("/api/login")
async def login(request_data: OAuth2PasswordRequestJSON, db: AsyncSession = Depends(get_db)):
    """ Api for login endpoint. """
    user = await authenticate_user(request_data.username, request_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = {"sub": user.username, "username": user.username}
    access_token = create_access_token(token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/people")
async def read_people(current_user: People = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """ Gets all the people infomation """
    result = await db.execute(select(people))
    columns = result.keys()
        # Convert each row into a dictionary with column names as keys
    data = [dict(zip(columns, row)) for row in result]
    return data


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')