#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-09-20 18:15:08
# @Author  : Nasir Ibrahim Abba
# @Description : something cool


from typing import List
from fastapi import APIRouter, Body, Query, Form, File, Path, UploadFile
from fastapi.param_functions import Depends

from sqlalchemy.orm.session import Session
from app.dependencies.dependencies import HasPermission, get_current_user, get_db
from app.user.schemas import UserSchema
from app.user_account import cruds, schemas

uac_router = APIRouter(
    prefix="/user_account",
    tags=["User Account Endpoints"]
)

Student_router = APIRouter(
    prefix="/student",
    tags=["student Endpoints"]
)
# ============[ Create Routes]============

@uac_router.post(
    "/create_by_image",
    response_model=schemas.UserAccountOut,
    # dependencies=[Depends(HasPermission(["can_create_any_user_account"]))],
)
async def create_uac_by_image(
    db: Session = Depends(get_db),
    user_account: schemas.UserAccountByImage = Depends(),
    user_image: UploadFile = File(...),
    user: UserSchema = Depends(get_current_user)
):
    return cruds.create_uac_by_image(db, user_account, user_image, user)


@uac_router.post(
    "/create_by_nin",
    response_model=schemas.UserAccountOut,
    # dependencies=[Depends(HasPermission(["can_create_any_user_account"]))],
)
async def create_uac_by_nin(
    db: Session = Depends(get_db),
    user_account: schemas.UserAccountByNIN = Body(...),
    user: UserSchema = Depends(get_current_user)
):
    return cruds.create_uac_by_nin(db, user_account, user)


@Student_router.post(
    "/create_by_nin",
    response_model=schemas.StudentOut,
    # dependencies=[Depends(HasPermission(["can_create_student"]))],
)
async def create_student_by_nin(
    db: Session = Depends(get_db),
    student: schemas.StudentCreateByNIN = Body(...),
    user: UserSchema = Depends(get_current_user)
):
    return cruds.create_student_by_nin(db, student, user)


# ============[ Read Routes]============

@uac_router.get(
    "/any/{uac_uuid}",
    response_model=schemas.UserAccountOut,
    # dependencies=[Depends(HasPermission(["can_view_any_user_account"]))],
)
async def get_uac_by_uuid(
    db: Session = Depends(get_db),
    uac_uuid: str = Path(...),
):
    return cruds.get_uac_by_uuid(db, uac_uuid)


@Student_router.get(
    "/id/{student_uuid}",
    response_model=schemas.StudentOut,
    # dependencies=[Depends(HasPermission(["can_view_student"]))],
)
async def get_student_by_uuid(
    db: Session = Depends(get_db),
    student_uuid: str = Path(...),
):
    return cruds.get_student_by_uuid(db, student_uuid)


# ============[ Update Routes]============



# ============[ List Routes]============
@uac_router.get(
    "/list/all",
    response_model=schemas.UserAccountList,
    # dependencies=[Depends(HasPermission(["can_view_all_user_account"]))],
)
async def list_all_uac(
    db: Session = Depends(get_db),
    filter: schemas.UserAccountFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
):
    return cruds.list_all_uac(db, filter, skip, limit)


@Student_router.get(
    "/list",
    response_model=schemas.StudentList,
    # dependencies=[Depends(HasPermission(["can_list_student"]))],
)
async def list_student(
    db: Session = Depends(get_db),
    filter: schemas.StudentFilter = Depends(),
    skip: int = 0,
    limit: int = 100,
):
    return cruds.list_student(db, filter, skip, limit)

# ============[ Delete Routes]============

@Student_router.delete(
    "/delete/{student_uuid}",
    # dependencies=[Depends(HasPermission(["can_delete_student"]))],
)
async def delete_student(
    db: Session = Depends(get_db),
    student_uuid: str = Path(...),
):
    return cruds.delete_student(db, student_uuid)