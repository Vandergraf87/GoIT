from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, text, or_, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Optional, Union
from datetime import date
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:admin@localhost/hw11"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Contact(Base):
    """
    Database model for storing contact information.

    :param id: The unique identifier for the contact.
    :param first_name: The first name of the contact.
    :param last_name: The last name of the contact.
    :param email: The email address of the contact.
    :param phone_number: The phone number of the contact.
    :param birthday: The birthday of the contact.
    :param additional_data: Additional data for the contact (optional).
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)

    def as_dict(self) -> Dict[str, str]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class ContactPydantic(BaseModel):
    """
    Pydantic model for serializing contact information.

    :param id: The unique identifier for the contact.
    :param first_name: The first name of the contact.
    :param last_name: The last name of the contact.
    :param email: The email address of the contact.
    :param phone_number: The phone number of the contact.
    :param birthday: The birthday of the contact.
    :param additional_data: Additional data for the contact (optional).
    """
    id: Union[str, int]
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: Union[str, date, None]
    additional_data: str = None

class ContactCreate(BaseModel):
    """
    Pydantic model for creating a new contact.

    :param first_name: The first name of the contact.
    :param last_name: The last name of the contact.
    :param email: The email address of the contact.
    :param phone_number: The phone number of the contact.
    :param birthday: The birthday of the contact.
    :param additional_data: Additional data for the contact (optional).
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str = None

class ContactUpdate(BaseModel):
    field: str
    value: Optional[Union[str, date]] = None

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()