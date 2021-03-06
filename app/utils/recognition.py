#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-07-20 15:10:26
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from app.utils.db import list_models_and_filter_by_equality
from app.dependencies.dependencies import get_recognition_auth_token
from fastapi import UploadFile
from app.utils.misc import requester
from sqlalchemy.orm.session import Session

from typing import Any, List
from os import getenv
import requests


def remote_search_faces(face_image: UploadFile, token: str) -> requests.Response:
    face_image.file.seek(0)
    payload = {"collection_id": getenv("RECOGNITION_COLLECTION", default=""), \
        "threshold": int(getenv("FACE_MATCH_THRESHOLD", default=99)), "max_faces": int(getenv("MAX_FACE_MATCHES", 1))}
    
    files = {"image_file": face_image.file.read()}
    
    headers = {"Authorization": f"Bearer {token}"}
    
    return requester(
        getenv("FACE_SEARCH_URL", ""),
        method="post",
        files=files,
        data=payload,
        headers=headers
    )


def remote_index_face(face_image_url: str, face_id: str, token: str) -> requests.Response:
    payload = {"CollectionId": getenv("RECOGNITION_COLLECTION", default=""), \
        "ExternalImageId": str(face_id), "ImagesURL": [face_image_url]}
    
    url = getenv("FACE_INDEX_URL", "")
    headers = {"Authorization": f"Bearer {token}"}

    return requester(
        url,
        method="post",
        json=payload,
        headers=headers
    )


def remote_detect_faces(face_image: UploadFile, token: str) -> requests.Response:
    face_image.file.seek(0)
    files = {"image_file": face_image.file.read()}
    
    headers = {"Authorization": f"Bearer {token}"}
    
    return requester(
        getenv("FACE_DETECT_URL", ""),
        method="post",
        files=files,
        headers=headers
    )


def index_account_model(model_list: List[Any]):
    for model in model_list:
        face_image_url: str = model.nin_info.image
        user_id: str = model.user_id
        index_face_to_collection(face_image_url, user_id)


def re_index_model(db: Session, model: Any, model_name: str, count_col: str):
    db_model_record = list_models_and_filter_by_equality(
        db, 
        model,
        {},
        model_name,
        count_by_column=count_col
    )

    count = int(db_model_record["count"])
    model_list: List[Any] = db_model_record["result"]

    if count % 100:
        rounds = (count // 100) + 1
    else:
        rounds = (count // 100)
    
    for i in range(1, rounds + 1):
        index_account_model(model_list)

        db_model_record = list_models_and_filter_by_equality(
            db, 
            model,
            {},
            model_name,
            skip= i * 100,
            count_by_column=count_col
        )

        model_list = db_model_record["result"]


def index_face_to_collection(face_image_url: str, face_id: str):
    try:
        token: str = get_recognition_auth_token()
        remote_index_face(face_image_url, face_id, token)
    except:
        pass


def detect_single_face(image: UploadFile, token: str):
    return remote_detect_faces(image, token).json()

