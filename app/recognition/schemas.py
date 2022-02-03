#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-07-17 14:52:20
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field



class BoundingBox(BaseModel):
    Height: float
    Left: float
    Top: float
    Width: float


class FaceOut(BaseModel):
    BoundingBox: BoundingBox
    Confidence: float
    ExternalImageId: str
    FaceId: str
    ImageId: str


class Face(BaseModel):
    Face: FaceOut
    Similarity: Optional[float] = None


class IndexFacesResponse(BaseModel):
    FaceModelVersion: str
    FaceRecords: List[Face]


class Image(BaseModel):
    Bytes: bytes


class SearchFaceResponse(BaseModel):
    FaceMatches: List[Face]
    FaceModelVersion: str
    SearchedFaceBoundingBox: BoundingBox
    SearchedFaceConfidence: float


class DectedFace(BaseModel):
    Confidence: float


class DetectFacesRequest(BaseModel):
    Attributes: Optional[List[str]] = ["ALL"]
    Image: Image


class DetectFacesResponse(BaseModel):
    FaceDetails: List[DectedFace]

