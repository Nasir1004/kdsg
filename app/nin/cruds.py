#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-10 07:10:52
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from typing import List

from fastapi.exceptions import HTTPException
from app.utils.db import create_model, delete_model_by_uuid, get_model_all, \
    get_model_by_name, get_model_by_nin, get_model_by_uuid, update_model_by_uuid

from app.nin import schemas, models
from sqlalchemy.orm.session import Session


def create_nin(db: Session, nin: schemas.NINCreate) -> models.NIN:
    return create_model(db, models.NIN, "NIN", nin)


def get_user_by_nin(db: Session, nin: str) -> models.NIN:
    return get_model_by_nin(db, models.NIN, "NIN", nin)


def general_get_user_by_nin(db: Session, nin: str) -> models.NIN:
    db_nin = get_user_by_nin(db, nin)
    if not db_nin:
        raise HTTPException(403, detail="Please retrieve and verify NIN first")
    return db_nin