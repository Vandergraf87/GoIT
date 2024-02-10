from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: Optional[str]
    email: str

    class Config:
        orm_mode = True

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    class Config:
        orm_mode = True

DATABASE_URL = "postgresql://postgres:admin@localhost/hw11"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Створення таблиць
    Base.metadata.create_all(bind=engine)

# Тепер викличіть `init_db()` перед викликом вашої програми
init_db()
