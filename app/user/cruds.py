from typing import Dict
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.access_control.models import Group

from app.user import schemas, models
from app.utils.misc import gen_random_password
from app.utils.user import get_password_hash, verify_password
from app.utils.db import create_model, get_model_by_field_first, list_models_and_filter_by_equality


def create_user(db: Session, user_data: schemas.UserCreate, autocommit=True, system_user=False):
    user_dict = user_data.dict()
    unhashed_password = user_dict.pop('password')
    hashed_password = get_password_hash(unhashed_password)
    user_dict['password_hash'] = hashed_password
    user = models.User(**user_dict)
    if system_user:
        user.is_system_user = True
    db.add(user)
    if autocommit:
        db.commit()
        db.refresh(user)
    else:
        db.flush()
    return user


def get_user_by_email(db: Session, email: EmailStr):
    return db.query(models.User).filter(models.User.email == email).first()


def check_user_exist(db: Session, email: EmailStr):
    db_user = get_user_by_email(db=db, email=email)
    if db_user:
        raise HTTPException(403, detail="User already exists")


def get_user_by_uuid(db: Session, uuid: str):
    return db.query(models.User).filter(models.User.uuid == str(uuid)).first()


def get_password_reset_by_uuid(db: Session, uuid: str):
    return db.query(models.PasswordReset). \
        filter(models.PasswordReset.uuid == uuid). \
        first()


def authenticate_user(email: EmailStr, password: str, dba: Session):
    user = get_user_by_email(db=dba, email=email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail='Email and password do not match'
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail='User is not active'
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail='Email and password do not match'
        )
    return schemas.UserSchema.from_orm(user) 



def change_system_user_password(db: Session, user_uuid: str):
    db_user: models.User = get_model_by_field_first(db, models.User, "uuid", "User", user_uuid)
    if not db_user:
        raise HTTPException(404, detail="User not found")
    password = gen_random_password()
    hashed_password = get_password_hash(password)
    
    db_user.password_hash = hashed_password
    db.commit()
    return schemas.PasswordChangeOut(password=password)

