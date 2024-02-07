from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date, text, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Union

DATABASE_URL = "postgresql://postgres:admin@localhost/hw11"
engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Contact(Base):
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
    id: Union[str, int]
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: Union[str, date]
    additional_data: str = None

Base.metadata.create_all(bind=engine)

app = FastAPI()

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str = None

class ContactUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone_number: str = None
    birthday: date = None
    additional_data: str = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/contacts/", response_model=ContactPydantic)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact.as_dict()

@app.get("/contacts/", response_model=List[ContactPydantic])
def read_contacts(q: str = None, db: Session = Depends(get_db)):
    if q:
        contacts = db.query(Contact).filter(
            or_(
                Contact.first_name.ilike(f"%{q}%"),
                Contact.last_name.ilike(f"%{q}%"),
                Contact.email.ilike(f"%{q}%")
            )
        ).all()
    else:
        contacts = db.query(Contact).all()

    contact_list = []
    for contact in contacts:
        contact_dict = contact.as_dict()
        contact_dict['id'] = str(contact.id)
        contact_dict['birthday'] = str(contact.birthday)
        contact_list.append(ContactPydantic(**contact_dict))

    return contact_list

@app.get("/contacts/{contact_id}", response_model=ContactPydantic)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact.as_dict()

@app.put("/contacts/{contact_id}", response_model=Dict[str, str])
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    for field, value in contact.dict().items():
        if value is not None:
            setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact.as_dict()

@app.delete("/contacts/{contact_id}", response_model=Dict[str, str])
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    return contact.as_dict()

@app.get("/contacts/birthday", response_model=List[ContactPydantic])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        text(f"EXTRACT(MONTH FROM birthday) = {today.month} AND EXTRACT(DAY FROM birthday) BETWEEN {today.day} AND {end_date.day}")
    ).all()
    return [contact.as_dict() for contact in contacts]