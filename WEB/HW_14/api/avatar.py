# avatar.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import cloudinary
from cloudinary.uploader import upload
from .config import CLOUDINARY_CONFIG
from .auth import get_current_user, User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
DATABASE_URL = "postgresql://postgres:admin@localhost/hw11"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()

@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if file.content_type.startswith("image/"):
        cloudinary.config(**CLOUDINARY_CONFIG)
        response = upload(file.file, folder="avatars")
        current_user.avatar_url = response["url"]

        db.add(current_user)
        db.commit()
        db.refresh(current_user)

        return {"message": "Avatar updated successfully", "avatar_url": response["url"]}
    else:
        raise HTTPException(status_code=400, detail="Invalid file format")
