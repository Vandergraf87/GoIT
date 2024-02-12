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
#from fastapi_limiter import Limiter
from fastapi_limiter.depends import RateLimiter

router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/contacts/", response_model=ContactPydantic, dependencies=[Depends(RateLimiter(times=5, minutes=1))])
def create_contact(
    contact: ContactCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a new contact.

    Parameters:
    - `contact` (ContactCreate): The contact data to create.
    - `current_user` (User): The current authenticated user.
    - `db` (Session): The database session.

    Returns:
    - `ContactPydantic`: The created contact.
    """
    db_contact = create_contact(db, contact, current_user.id)
    return ContactPydantic(**db_contact.as_dict())

def get_user_contacts(db: Session, user_id: int, q: str = None):
    """
    Retrieve contacts for a specific user, optionally filtering by first name, last name, or email.

    :param db: The database session.
    :type db: sqlalchemy.orm.Session

    :param user_id: The ID of the user for whom contacts should be retrieved.
    :type user_id: int

    :param q: The search query to filter contacts by first name, last name, or email (case-insensitive).
    :type q: str, optional

    :return: A list of contacts that match the search criteria.
    :rtype: List[Contact]
    """
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
    """
    Retrieve a contact by ID.

    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int

    :param current_user: The currently authenticated user.
    :type current_user: User, optional

    :param db: The database session.
    :type db: sqlalchemy.orm.Session

    :return: The details of the retrieved contact.
    :rtype: ContactPydantic

    :raises HTTPException 404: If the contact with the specified ID is not found.
    :raises HTTPException 403: If the authenticated user does not have permission to access the contact.
    """
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
    """
    Update contact information.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int

    :param updates: A list of ContactUpdate objects representing the fields and values to update.
    :type updates: List[ContactUpdate]

    :param current_user: The currently authenticated user.
    :type current_user: User, optional

    :param db: The database session.
    :type db: sqlalchemy.orm.Session

    :return: A dictionary containing the updated contact information.
    :rtype: Dict[str, str]

    :raises HTTPException 404: If the contact with the specified ID is not found.
    :raises HTTPException 403: If the authenticated user does not have permission to update the contact.
    """
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
    """
    Delete a contact from the database.

    :param contact_id: The ID of the contact to be deleted.
    :param current_user: The current authenticated user.
    :param db: The database session.

    :return: A dictionary with a message confirming the deletion.
    """
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
    """
    Get a list of contacts with upcoming birthdays within the next 7 days.

    :param current_user: The current authenticated user.
    :param db: The database session.

    :return: A list of contacts with upcoming birthdays.
    """
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
    """
    Register a new user.

    :param user: The user data for registration.
    :param db: The database session.

    :return: The registered user with additional details.
    """
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