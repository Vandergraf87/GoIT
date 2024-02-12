import unittest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from main import app
from datetime import date, timedelta
from sqlalchemy.orm import Session
from api.auth import SECRET_KEY, verify_password, create_access_token
from api.models import get_db, Contact, ContactCreate, ContactPydantic
from api.auth_schemas import User, ALGORITHM
from api.api import upcoming_birthdays
from passlib.context import CryptContext
import jwt

class TestContactAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.session = MagicMock(spec=Session)
        self.client.app.dependency_overrides[get_db] = lambda: self.session

    def tearDown(self):
        self.client.app.dependency_overrides.clear()

    def test_create_contact(self):
        user_id = 1  
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "123456789",
            "birthday": "2000-01-01",
            "additional_data": "Some additional data",
        }
        response = self.client.post(f"/contacts/?user_id={user_id}", json=contact_data)
        self.assertEqual(response.status_code, 200)
        created_contact = response.json()
        self.assertEqual(created_contact["first_name"], contact_data["first_name"])

class TestVerifyPassword(unittest.TestCase):
    def setUp(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def test_verify_password(self):
        hashed_password = self.pwd_context.hash("secret_password")
        plain_password = "secret_password"

        result = verify_password(plain_password, hashed_password)

        self.assertTrue(result)

    def test_verify_password_invalid(self):
        hashed_password = self.pwd_context.hash("correct_password")
        plain_password = "incorrect_password"

        result = verify_password(plain_password, hashed_password)

        self.assertFalse(result)

class TestCreateAccessToken(unittest.TestCase):

    def test_create_access_token_without_expiration(self):
        data = {"sub": "test_user"}
        token = create_access_token(data)

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        self.assertEqual(decoded_token["sub"], data["sub"])

    def test_create_access_token_with_expiration(self):
        data = {"sub": "test_user"}
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, expires_delta)

        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        self.assertEqual(decoded_token["sub"], data["sub"])

        expiration_time = datetime.utcfromtimestamp(decoded_token["exp"])
        expected_expiration_time = datetime.utcnow() + expires_delta
        self.assertLessEqual(expiration_time, expected_expiration_time)

class TestUpcomingBirthdays(unittest.TestCase):

    def test_upcoming_birthdays(self):
        mock_user = User(id=1, username="test_user")
        mock_db = Session()

        upcoming_birthday_contact = Contact(
            first_name="Upcoming",
            last_name="Birthday",
            email="birthday@example.com",
            phone_number="123456789",
            birthday=date.today() + timedelta(days=3),
            user_id=mock_user.id
        )
        mock_db.add(upcoming_birthday_contact)
        mock_db.commit()

        result = upcoming_birthdays(current_user=mock_user, db=mock_db)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["first_name"], "Upcoming")
        self.assertEqual(result[0]["last_name"], "Birthday")

if __name__ == "__main__":
    unittest.main()