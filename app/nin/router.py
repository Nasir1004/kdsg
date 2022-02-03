#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-10 09:18:22
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from app.utils.nin import gen_nin_from_dict, get_nin_from_store
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from app.dependencies.dependencies import HasPermission, get_current_user, get_db, get_nin_auth_token
from app.nin import cruds, schemas
from app.user.schemas import UserSchema


nin_router = APIRouter(
    prefix="/nin",
    tags=["NIN Endpoints"]
)


# ============[ Create Routes]============


# ============[ Read Routes]============
# todo: make requests time out for nin retrieval from store, also check store
@nin_router.get(
    "/{nin}",
    response_model=schemas.NINOut,
    # dependencies=[Depends(HasPermission(["can_retrieve_nin_data"]))]
)
async def get_nin_data(
    nin: str,
    db: Session = Depends(get_db),
    nin_token: str = Depends(get_nin_auth_token),
    user: UserSchema = Depends(get_current_user)
):
    nin_db = cruds.get_user_by_nin(db, nin)

    if nin_db:
        return nin_db
    
    nin_from_store: dict = get_nin_from_store(nin, nin_token)
    nin_model: schemas.NINCreate = gen_nin_from_dict(nin_from_store, str(user.uuid))
    db_nin = cruds.create_nin(db, nin_model)
    return db_nin


# ============[ Update Routes]============


# ============[ Delete Routes]============