from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Union
from datetime import date, datetime, timedelta
from sqlalchemy import or_, extract
from .models import Contact, ContactPydantic, ContactCreate, ContactUpdate, get_db

router = APIRouter()

@router.post("/contacts/", response_model=ContactPydantic)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact.as_dict()


@router.get("/contacts/", response_model=List[ContactPydantic])
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

@router.get("/contacts/{contact_id}", response_model=ContactPydantic)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return db_contact.as_dict()

@router.patch("/contacts/{contact_id}", response_model=Dict[str, str])
def patch_contact(contact_id: int, updates: List[ContactUpdate], db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")

    for update in updates:
        field = update.field
        value = update.value

        if field == "birthday" and value is not None:
            value = datetime.strptime(value, "%Y-%m-%d").date()

        if value is not None:
            setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact.as_dict()

@router.delete("/contacts/{contact_id}", response_model=Dict[str, str])
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    return contact.as_dict()

@router.get("/contacts/birthday", response_model=List[ContactPydantic])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    end_date = today + timedelta(days=7)

    birthday_month = extract('month', Contact.birthday)
    birthday_day = extract('day', Contact.birthday)

    contacts = (
        db.query(Contact)
        .filter(
            (
                (birthday_month == today.month)
                & (birthday_day >= today.day)
                & (birthday_day <= end_date.day)
            )
            | (
                (birthday_month == (today.month % 12) + 1)
                & (birthday_day <= end_date.day)
            )
        )
        .all()
    )

    return [ContactPydantic(**contact.as_dict()) for contact in contacts]