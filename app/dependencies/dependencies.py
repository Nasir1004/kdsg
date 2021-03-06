#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-06 20:59:07
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from datetime import timedelta
from typing import Dict
from jose import jwt # type: ignore
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from os import getenv

from app.config import database as db
from app.user import cruds as users_cruds, schemas as users_schema
from app.utils.timing import get_current_datetime


load_dotenv()


SECRET_KEY = getenv('JWT_SECRET_KEY')
TOKEN_URL: str = getenv('DOCS_AUTH_URL', default="")
ALGORITHM = getenv("JWT_ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_db():
    dbase = db.SessionLocal()
    try:
        yield dbase
    finally:
        dbase.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user = users_schema.UserSchema.from_orm(
        users_cruds.get_user_by_email(db=db, email=payload['data']['email'])
    )
    return user


def verify_vision_token(token: str = Depends(oauth2_scheme)) -> Dict:
    vision_secret_key = getenv("VISION_JWT_KEY", "")
    vision_algo = getenv("VISION_JWT_ALG", "")
    
    payload = jwt.decode(token, vision_secret_key, algorithms=[vision_algo])

    return payload


def has_vision_search_perm(payload: Dict = Depends(verify_vision_token)):
    if "can_search_faces" in payload["data"]["permissions"]:
        return True
    
    raise HTTPException(403, detail="Unauthorized access to endpoint")


def has_detect_face_perm(payload: Dict = Depends(verify_vision_token)):
    if "can_detect_image_face" in payload["data"]["permissions"]:
        return True
    
    raise HTTPException(403, detail="Unauthorized access to endpoint")

def get_auth_token(token: str = Depends(oauth2_scheme)):
    return token


def get_nin_auth_token():
    expires = get_current_datetime() + timedelta(hours=int(getenv("TOKEN_LIFE_SPAN")))
    data = {"exp": expires, "data": {"permissions": ["can_retrieve_nin_data"]}}
    token = jwt.encode(data, getenv("NIN_JWT_KEY"), algorithm=getenv("NIN_JWT_ALG"))
    return token


def get_recognition_auth_token():
    expires = get_current_datetime() + timedelta(hours=int(getenv("TOKEN_LIFE_SPAN")))
    data = {"exp": expires, "data": {"permissions": ["can_search_faces", "can_index_faces", "can_detect_image_face"], \
        "email": getenv("MACHINE_NAME", "")}}
    token = jwt.encode(data, getenv("VISION_JWT_KEY"), algorithm=getenv("VISION_JWT_ALG"))
    return token

class HasPermission:
    def __init__(self, perms: list):
        self.perms = perms

    def __call__(
        self, user: users_schema.UserSchema = Depends(get_current_user)
        ):

        for perm in self.perms:
            if perm not in user.permissions:
                raise HTTPException(
                    status_code=403,
                    detail='Permission denied'
                )
