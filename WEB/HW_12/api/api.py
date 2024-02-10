from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Union
from datetime import date, datetime, timedelta
from sqlalchemy import or_, extract
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .models import Contact, ContactPydantic, ContactCreate, ContactUpdate, get_db
from passlib.context import CryptContext
from .auth_schemas import UserCreate, UserLogin, User, UserDB, UserDBInResponse
from .auth import pwd_context, get_current_user, verify_password, create_access_token

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/contacts/", response_model=ContactPydantic)
def create_contact(
    contact: ContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_contact = create_contact(db, contact, current_user.id)
    return ContactPydantic(**db_contact.as_dict())

def get_user_contacts(db: Session, user_id: int, q: str = None):
    query = db.query(Contact).filter(Contact.user_id == user_id)
    if q:
        query = query.filter(
            db.or_(
                Contact.first_name.ilike(f"%{q}%"),
                Contact.last_name.ilike(f"%{q}%"),
                Contact.email.ilike(f"%{q}%")
            )
        )
    return query.all()

@router.get("/contacts/", response_model=List[ContactPydantic])
def read_contacts(
    q: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    contacts = get_user_contacts(db, current_user.id, q)
    return [ContactPydantic(**contact.as_dict()) for contact in contacts]

@router.get("/contacts/{contact_id}", response_model=ContactPydantic)
def get_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    return ContactPydantic(**db_contact.as_dict())

@router.patch("/contacts/{contact_id}", response_model=Dict[str, str])
def patch_contact(
    contact_id: int,
    updates: List[ContactUpdate],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

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
def delete_contact(
    contact_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    delete_contact(db, db_contact)
    return db_contact.as_dict()

@router.get("/contacts/birthday", response_model=List[ContactPydantic])
def upcoming_birthdays(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
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
        .filter(Contact.user_id == current_user.id)
        .all()
    )

    return [ContactPydantic(**contact.as_dict()) for contact in contacts]

@router.post("/register/", response_model_include=UserDBInResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    hashed_password = pwd_context.hash(user.password)

    db_user = UserDB(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    db_user.token = create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)

    return db_user

@router.post("/token/", response_model=dict)
def login_user(form_data: UserLogin = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user.token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": user.token, "token_type": "bearer"}