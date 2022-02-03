#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-07-16 22:37:46
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from os import getenv
from app.utils.recognition import re_index_model, remote_detect_faces, remote_index_face, remote_search_faces
from app.dependencies.dependencies import get_recognition_auth_token
from app.utils.db import get_model_by_field_first
from fastapi import HTTPException, UploadFile

from dotenv import load_dotenv
import ulid

from sqlalchemy.orm.session import Session

from app.recognition import schemas
from app.user import schemas as user_schemas

load_dotenv()

# =========[ Recognition CRUDs ]==========

# Creates

def get_face(
    face_image: UploadFile,
    token: str,
) -> schemas.SearchFaceResponse:
    search_response = remote_search_faces(face_image, token)

    if search_response.status_code > 299:
        raise HTTPException(403, detail="Error occurred during face search, match not found try again...")
    
    face_match: schemas.SearchFaceResponse = schemas.SearchFaceResponse(**search_response.json())
    if not face_match.FaceMatches:
        raise HTTPException(404, detail="No match found!")
    
    try:
        user_id: str = face_match.FaceMatches[0].Face.ExternalImageId
    except ValueError:
        raise HTTPException(403, detail="Match found but returned invalid user_id")
    
    return face_match


def get_face_id(face_image: UploadFile, token: str):
    face_match = get_face(face_image, token)
    similarity = face_match.FaceMatches[0].Similarity
    
    if similarity and similarity < float(getenv("FACE_MATCH_THRESHOLD", 99)):
        raise HTTPException(400, detail="Face not recognized")
    
    return face_match.FaceMatches[0].Face.ExternalImageId

def index_face_to_collection(face_image_url: str, face_id: str):
    try:
        token: str = get_recognition_auth_token()
        remote_index_face(face_image_url, face_id, token)
    except:
        pass
    
    # todo: handle the case where indexing fails, we do not return the result
    # todo: of this function, as we do not expect it to have any usage i.e
    # todo: we do not intend to have this function be a bottleneck to user
    # todo: account creation 


def detect_image_face(image: UploadFile, token: str):
    return remote_detect_faces(image, token).json()


def detect_single_face(image: UploadFile):
    response = remote_detect_faces(image, get_recognition_auth_token()).json()
    detect_face_result = schemas.DetectFacesResponse(**response)

    if len(detect_face_result.FaceDetails) != 1:
        raise HTTPException(400, detail="Error, exactly one face is required in the uploaded image")
    
    if detect_face_result.FaceDetails[0].Confidence < int(getenv("FACE_CONFIDENCE_THRESHOLD", 0)):
        raise HTTPException(400, detail="Image quality is too poor, inadequate face detection")
    
    return True


def check_for_single_face(image: UploadFile):
    if not detect_single_face(image):
        raise HTTPException(403, detail="No face detected, please make sure image contain a single clear face")
    

# Reads


# Updates


# Lists


# Deletes


# helpers
