#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-07-16 21:56:24
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.orm.session import Session
from app.dependencies.dependencies import HasPermission, get_db, get_recognition_auth_token, has_detect_face_perm, has_vision_search_perm

from app.recognition import cruds, schemas
from app.user import schemas as user_schemas


recognition_router = APIRouter(
    prefix="/facial_recognition",
    tags = ["Facial Recognition Endpoints"]
)

# ============[ CREATE Routes]============

@recognition_router.post(
    "/detect_image_face",
    response_model=schemas.DetectFacesResponse,
    # dependencies=[Depends(HasPermission(["can_detect_image_face"]))]
)
async def detect_image_face(
    image: UploadFile = File(...),
    token: str = Depends(get_recognition_auth_token),
):
    return cruds.detect_image_face(image, token)



# ============[ READ Routes]============


# ============[ UPDATE Routes]============


# ============[ LIST Routes]============


# ============[ DELETE Routes]============

