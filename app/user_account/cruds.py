#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-09-20 22:25:23
# @Author  : Nasir Ibrahim Abba
# @Description : something cool

from unicodedata import category
from app.utils.enums import LoanPaymentStatus
from os import getenv
from typing import Optional, Union, List
from app.utils.misc import gen_email, gen_random_password
from app.dependencies.dependencies import get_recognition_auth_token
from datetime import date, datetime, timedelta
from app.utils.nin import gen_user_from_nin
import ulid
from app.nin.cruds import general_get_user_by_nin, get_user_by_nin
from app.nin.models import NIN
from app.recognition.cruds import check_for_single_face, detect_single_face, get_face_id, index_face_to_collection
from app.utils.image_qr import create_and_upload_qr_cloud, upload_image_file_to_cloud, upload_remote_image_to_cloud
from fastapi import UploadFile, HTTPException
from app.user.schemas import UserCreate, UserSchema, UserUpdate
from app.user.cruds import check_user_exist, create_user
from app.user.models import User
from sqlalchemy.orm.session import Session
from app.utils.db import get_model_all, check_model_exists, update_model_by_uuid, check_model_is_duplicate, create_model, delete_model_by_field, list_models_and_filter_by_equality, get_model_by_field_first, update_model_by_field

from app.user_account import schemas, models


# =========[ Create ]=========

def create_uac_by_image(
    db: Session, 
    user_account: schemas.UserAccountByImage, 
    user_image: UploadFile, 
    current_user: UserSchema,
    autocommit: bool = True
):
    check_for_single_face(user_image)
    db_user: User = create_user(db, user_account.user, autocommit=False)
    if user_account.next_of_kin:
        db_next_of_kin: models.NextOfKin = create_model(db, models.NextOfKin, "Next Of Kin", user_account.next_of_kin,\
        autocommit=False)
        next_of_kin_uuid: Optional[str] = str(db_next_of_kin.uuid)
    else:
        next_of_kin_uuid = None

    try:
        user_image_url = upload_image_file_to_cloud(user_image, "USERS_IMAGE_BUCKET")
    except:
        raise HTTPException(500, "User image upload failed")
    
    to_create = schemas.UserAccountCreate(user_uuid=str(db_user.uuid), image=user_image_url, phone=user_account.phone,\
        address=user_account.address, gender=user_account.gender, birthdate=user_account.birthdate, \
        next_of_kin_uuid=next_of_kin_uuid, creator_uuid=str(current_user.uuid))
    
    db_user_account = create_model(db, models.UserAccount, "User Account", to_create, autocommit=False)
    if autocommit:
        db.commit()
        db.refresh(db_user_account)

    return db_user_account


def create_uac_by_nin(
    db: Session, 
    user_account: schemas.UserAccountByNIN, 
    user: UserSchema,
    autocommit: bool = True
):
    check_model_is_duplicate(db, models.UserAccount, {"nin": user_account.nin}, "User Account")
    db_nin_info: NIN = general_get_user_by_nin(db, user_account.nin)
    check_user_exist(db, user_account.email)
    # user_image_url = upload_remote_user_image(db_nin_info.image, "USERS_IMAGE_BUCKET")

    to_create = gen_user_from_nin(db_nin_info)
    to_create.email = user_account.email
    db_user: User = create_user(db, to_create, autocommit=False)

    if user_account.next_of_kin:
        nextofkin: models.NextOfKin = create_model(db, models.NextOfKin, "Next Of Kin", user_account.next_of_kin, autocommit=False)
        next_of_kin_uuid: Optional[str] = str(nextofkin.uuid)
    else:
        next_of_kin_uuid = None
    
    to_create = schemas.UserAccountCreate(user_uuid=str(db_user.uuid), nin=db_nin_info.nin, image =db_nin_info.image, phone=db_nin_info.phone if db_nin_info.phone else user_account.phone, \
        address=user_account.address, gender=db_nin_info.gender, \
        birthdate=datetime.strptime(db_nin_info.birthdate, "%d-%m-%Y").date(), \
        next_of_kin_uuid=next_of_kin_uuid, creator_uuid=str(user.uuid))

    db_user_account = create_model(db, models.UserAccount, "User Account", to_create, autocommit=False)
    if autocommit:
        db.commit()
        db.refresh(db_user_account)
    return db_user_account


def create_student_by_nin(
    db: Session, 
    student: schemas.StudentCreateByNIN,
    user: UserSchema
):
    db_uac = check_duplicate_uac_by_nin(db, student.nin)
    email = gen_email()
    uac_to_create = schemas.UserAccountByNIN(nin=student.nin, email=email, \
    address=student.address, phone=student.phone)
    db_uac: models.UserAccount = create_uac_by_nin(db, uac_to_create, user, autocommit=False)
    
    coordinator = schemas.CoordinatorCreate(firstname=student.coordinator_firstname, lastname=student.coordinator_lastname, \
        middlename=student.coordinator_middlename, phone=student.coordinator_phone, address=student.coordinator_address)
    
    db_coordinator: models.Coordinator = create_model(db, models.Coordinator, "Coordinator", coordinator, autocommit=False)
    coordinator_uuid = str(db_coordinator.uuid)

    to_create = schemas.StudentCreate(user_account_uuid=str(db_uac.uuid),  coordinator_uuid=coordinator_uuid, \
        creator_uuid=str(user.uuid), marital_status=student.marital_status, riwaya=student.riwaya, \
        category=student.category, qualification=student.qualification,language_spoken=student.language_spoken, lga=student.lga)
    
    db_student: models.Student = create_model(db, models.Student, "student", to_create)
    return db_student


# =========[ Read 53396084303    69414147651]=========

def get_uac_by_uuid(
    db: Session, 
    uac_uuid: str
):
    db_uac: models.UserAccount = get_model_by_field_first(db, models.UserAccount, "uuid", "User Account", uac_uuid)
    if not db_uac:
        raise HTTPException(404, detail="User Account not found")
    return db_uac


def get_uac_by_image(
    db: Session,
    user_image: UploadFile
):
    try:
        uac_uuid = get_face_id(user_image, get_recognition_auth_token())
    except:
        raise HTTPException(404, detail="Face ID not found")
    
    return get_model_by_field_first(db, models.UserAccount, "uuid", "User Account", uac_uuid)


def get_student_by_uuid(
    db: Session, 
    student_uuid: str
):
    return get_model_by_field_first(db, models.Student, "uuid", "Student", student_uuid)


# =========[ Update ]=========

def update_student_by_uuid(db: Session, student: schemas.StudentUpdate, student_uuid: str) -> models.Student:
    return update_model_by_uuid(db, models.Student, student, "Student", student_uuid)


def uac_image_update(
    db: Session, 
    user_image: UploadFile, 
    uac_uuid: str,
    autocommit = True,
):
    db_uac: models.UserAccount = check_model_exists(db, models.UserAccount, {"uuid": uac_uuid}, "User Account")
    try:
        user_image_url = upload_image_file_to_cloud(user_image, "USERS_IMAGE_BUCKET")
    except:
        raise HTTPException(500, "User image upload failed")
    
    db_uac.image = user_image_url
    if autocommit:
        db.commit()
        db.refresh(db_uac)
    
    return db_uac


# =========[ List ]=========

def list_all_uac(
    db: Session, 
    filter: schemas.UserAccountFilter, 
    skip: int, 
    limit: int
):
    fields = {"nin": filter.nin, "birthdate": filter.birthdate}
    join_fields = {
        User: {"firstname": filter.firstname, "lastname": filter.lastname, \
            "middlename": filter.middlename, "email": filter.email, "phone": filter.phone}
    }

    return list_models_and_filter_by_equality(db, models.UserAccount, fields, "User Account", \
        limit=limit, skip=skip, count_by_column="uuid", join_fields=join_fields)


def get_student_all(db: Session, limit: int = 100, skip: int = 0) -> List[models.Student]:
    return get_model_all(db, models.Student, limit, skip)


def list_students(
    db: Session, 
    filter: schemas.StudentFilter,
    skip: int, 
    limit: int
):
    
    join_fields = {
        models.UserAccount: {"phone": filter.phone, "nin": filter.nin}
    }

    return list_models_and_filter_by_equality(db, models.Student, " Student", \
        limit=limit, skip=skip, join_fields=join_fields)


# =========[ Delete ]=========

def delete_student(db: Session, student_uuid: str):
    db_student: models.Student = check_model_exists(db, models.Student, \
        {"uuid": student_uuid}, "student")
    db_student_uac: models.UserAccount = db_student.user_account
    db_student_user: User = db_student_uac.user
    delete_model_by_field(db, models.Student, "student", {"uuid": student_uuid}, autocommit=False)
    delete_model_by_field(db, models.UserAccount, "User Account", \
        {"uuid": str(db_student_uac.uuid)}, autocommit=False)
    return delete_model_by_field(db, User, "User", {"uuid": str(db_student_user.uuid)}, autocommit=True)


# =========[ Helpers ]=========

def upload_remote_user_image(image_url: str, bucket_var_name: str):
    filename = f"{str(ulid.new())}.png"

    image_url = upload_remote_image_to_cloud(image_url, filename, bucket_var_name)
    if not image_url:
        raise HTTPException(403, detail="Could not upload user image to cloud")
    
    return image_url


def check_duplicate_student_by_image(db: Session, student_image: UploadFile):
    try:
        db_uac: models.UserAccount = get_uac_by_image(db, student_image)
        if db_uac:
            raise HTTPException(409)
    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(409, detail="student already exists, duplicate student not allowed")


def check_duplicate_uac_by_nin(db: Session, nin: str):
    try:
        db_uac: models.UserAccount = get_model_by_field_first(db, models.UserAccount, "nin", "User Account", nin)
        if db_uac:
            raise HTTPException(409)
        
    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(409, detail="student already exists, duplicate student not allowed")


def verify_student_creds(
    db: Session, 
    student: Union[schemas.StudentCreateByImage, schemas.StudentCreateByNIN]
):
    check_model_is_duplicate(db, models.Student, \
        {"phone": student.phone}, "phone Number")


def get_all_student_by_category(db: Session, category: str) -> List[models.Student]:
    return db.query(models.Student).filter(models.Student.category == category).all()
