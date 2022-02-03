#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-10 06:28:00
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from typing import Optional
from pydantic import BaseModel, Field

from app.mixins.schemas import BaseSchemaMixin
from app.utils.enums import Gender, NINType


class NINCreate(BaseModel):
    nin: str = Field(..., max_length=16)
    firstname: str = Field(..., max_length=45)
    lastname: str = Field(..., max_length=45)
    middlename: Optional[str] = Field(None, max_length=45)
    address: str = Field(..., max_length=160)
    phone: str = Field(..., max_length=16)
    gender: Gender
    birthdate: str = Field(..., min_length=6, max_length=16)
    image: str = Field(..., max_length=160)
    pulled_by: str
    nin_type: Optional[NINType] = NINType.national


class NINSchema(BaseSchemaMixin):
    nin: str = Field(..., max_length=16)
    firstname: str = Field(..., max_length=45)
    lastname: str = Field(..., max_length=45)
    middlename: Optional[str] = Field(None, max_length=45)
    address: str = Field(..., max_length=160)
    phone: str = Field(..., min_length=8, max_length=16)
    gender: Gender
    birthdate: str = Field(..., min_length=6, max_length=16)
    image: str = Field(..., max_length=160)
    pulled_by: str
    nin_type: Optional[NINType] = None

    class Config:
        orm_mode = True


class NINOut(BaseSchemaMixin):
    nin: str = Field(..., max_length=16)
    firstname: str = Field(..., max_length=45)
    lastname: str = Field(..., max_length=45)
    middlename: Optional[str] = Field(None, max_length=45)
    address: str = Field(..., max_length=160)
    phone: str = Field(..., min_length=8, max_length=16)
    gender: Gender
    birthdate: str = Field(..., min_length=6, max_length=16)
    image: str = Field(..., max_length=160)
    nin_type: Optional[NINType] = None

    class Config:
        orm_mode = True

