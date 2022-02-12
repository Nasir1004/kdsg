#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-09-20 17:22:39
# @Author  : Nasir Ibrahim Abba
# @Description : something cool


from ast import Str
from re import L, M
from unittest import result
from pydantic.networks import EmailStr
from app.utils.enums import Gender, Category, Marital_Status, Riwaya, Language
from app.mixins.commons import ListBase, LoanTypeMin, UserAccountMinPublic, UserMin, LoanBeneficiaryMid, LoanBeneficiaryFull, LoanBeneficiaryMin, VehicleMin
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional
from app.mixins.schemas import BaseSchemaMixin
from app.utils.custom_validators import checkbirthdate, cleaned, uppercased
from datetime import date
from app.user.schemas import UserOut, UserCreate


class NextOfKinCreate(BaseModel):
    firstname: str = Field(..., max_length=45, description="first name of next of kin")
    lastname: str = Field(..., max_length=45, description="last name of next of kin")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of next of kin")
    phone: str = Field(..., max_length=20, description="phone number of next of kin")
    address: str = Field(..., max_length=100, description="address of next of kin")

    _val_firstname = uppercased("firstname")
    _val_lastname = uppercased("lastname")
    _val_middlename = uppercased("middlename")
    _val_address = uppercased("address")


class NextOfKinUpdate(BaseModel):
    firstname: Optional[str] = Field(None, max_length=45, description="first name of next of kin")
    lastname: Optional[str] = Field(None, max_length=45, description="last name of next of kin")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of next of kin")
    phone: Optional[str] = Field(None, max_length=20, description="phone number of next of kin")
    address: Optional[str] = Field(None, max_length=100, description="address of next of kin")

    _val_firstname = uppercased("firstname")
    _val_lastname = uppercased("lastname")
    _val_middlename = uppercased("middlename")
    _val_address = uppercased("address")


class NextOfKinOut(BaseSchemaMixin):
    firstname: str = Field(..., max_length=45, description="first name of next of kin")
    lastname: str = Field(..., max_length=45, description="last name of next of kin")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of next of kin")
    phone: str = Field(..., max_length=20, description="phone number of next of kin")
    address: str = Field(..., max_length=100, description="address of next of kin")


class NextOfKinList(ListBase):
    result: List[NextOfKinOut]


class CoordinatorCreate(BaseModel):
    firstname: str = Field(..., max_length=45, description="first name of coordinattor")
    lastname: str = Field(..., max_length=45, description="last name of coordinator")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of coordinator")
    phone: str = Field(..., max_length=20, description="phone number of coordinator")
    address: str = Field(..., max_length=100, description="address of coordinator")

    _val_firstname = uppercased("firstname")
    _val_lastname = uppercased("lastname")
    _val_middlename = uppercased("middlename")
    _val_address = uppercased("address")


class CoordinatorUpdate(BaseModel):
    firstname: Optional[str] = Field(None, max_length=45, description="first name of coordinator")
    lastname: Optional[str] = Field(None, max_length=45, description="last name of coordinator")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of coordinator")
    phone: Optional[str] = Field(None, max_length=20, description="phone number of coordinator")
    address: Optional[str] = Field(None, max_length=100, description="address of coordinator")

    _val_firstname = uppercased("firstname")
    _val_lastname = uppercased("lastname")
    _val_middlename = uppercased("middlename")
    _val_address = uppercased("address")


class CoordinatorOut(BaseSchemaMixin):
    firstname: str = Field(..., max_length=45, description="first name of coordinator")
    lastname: str = Field(..., max_length=45, description="last name of coordinator")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of coordinator")
    phone: str = Field(..., max_length=20, description="phone number of coordinator")
    address: str = Field(..., max_length=100, description="address of coordinator")


class CoordinatorList(ListBase):
    result: List[CoordinatorOut]


class UserAccountByImage(BaseModel):
    user: UserCreate
    phone: str = Field(..., max_length=20, description="Phone number of the user")
    address: str = Field(..., max_length=255, description="Address of user")
    gender: Gender
    birthdate: date = Field(..., description="birthdate of user")
    next_of_kin: Optional[NextOfKinCreate] = Field(None)

    _val_address = uppercased("address")


class UserAccountByNIN(BaseModel):
    nin: str = Field(..., max_length=16, description="National Identity Number")
    email: EmailStr
    address: str = Field(..., max_length=255, description="Address of user")
    phone: str = Field(..., max_length=20, description="Phone number")
    next_of_kin: Optional[NextOfKinCreate] = Field(None, description="next of kin details")


class UserAccountCreate(BaseModel):
    user_uuid: str = Field(..., description="unique id of user")
    next_of_kin_uuid: Optional[str] = Field(None, description="unique id of next of kin")
    nin: Optional[str] = Field(None, max_length=16, description="nin of user")
    phone: str = Field(..., max_length=20, description="Phone number of the user")
    address: str = Field(..., description="address of user")
    image: str = Field(..., max_length=255, description="image of user")
    gender: Gender
    birthdate: date
    creator_uuid: str


class UserAccountUpdate(BaseModel):
    user_uuid: Optional[str] = Field(None, description="unique id of user")
    next_of_kin_uuid: Optional[str] = Field(None, description="unique id of next of kin")
    nin: Optional[str] = Field(None, max_length=16, description="nin of user")
    phone: Optional[str] = Field(None, max_length=20, description="Phone number of the user")
    address: Optional[str] = Field(None, description="address of user")
    image: Optional[str] = Field(None, max_length=255, description="image of user")
    gender: Optional[Gender] = Field(None)
    birthdate: Optional[date] = Field(None)


class UserAccountFilter(BaseModel):
    firstname: Optional[str] = Field(None, max_length=45)
    lastname: Optional[str] = Field(None, max_length=45)
    middlename: Optional[str] = Field(None, max_length=45)
    email: Optional[EmailStr] = Field(None)
    phone: Optional[str] = Field(None, max_length=20)
    nin: Optional[str] = Field(None, max_length=16, description="nin of user")
    birthdate: Optional[date] = Field(None)


class UserAccountOut(BaseSchemaMixin):
    user_uuid: str = Field(..., description="unique id of user")
    next_of_kin_uuid: Optional[str] = Field(None, description="unique id of next of kin")
    nin: Optional[str] = Field(None, max_length=16, description="nin of user")
    image: str = Field(..., max_length=255, description="image of user")
    phone: str = Field(..., max_length=20, description="Phone number of the user")
    address: str = Field(..., description="address of user")
    gender: Gender
    birthdate: date

    user: UserMin


class UserAccountList(ListBase):
    result: List[UserAccountOut]


class StudentCreateByNIN(BaseModel):
    nin: str = Field(..., max_length=16, description="National Identity Number")
    phone: str = Field(..., max_length=20, description="phone number of student")
    address: str = Field(..., max_length=255, description="Address of student")
    lga: str = Field(..., max_length=255, description="lga of student")
    coordinator_firstname: str = Field(..., max_length=45, description="first name of coordinator")
    coordinator_lastname: str = Field(..., max_length=45, description="last name of coordinator")
    coordinator_middlename: Optional[str] = Field(None, max_length=45, description="middle name of coordinator")
    coordinator_phone: str = Field(..., max_length=20, description="phone number of coordinator")
    coordinator_address: str = Field(..., max_length=100, description="address of coordinator")
    marital_status: Marital_Status
    qualification: str
    language_spoken: str
    riwaya: str
    category: str

    _val_address = uppercased("address")
    _val_address = uppercased("lga")


class StudentCreateByImage(BaseModel):
    firstname: str = Field(..., max_length=45, description="first name of student")
    lastname: str = Field(..., max_length=45, description="last name of student")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of student")
    phone: str = Field(..., max_length=20, description="phone number of student")
    address: str = Field(..., max_length=255, description="address of student")
    coordinator_firstname: str = Field(..., max_length=45, description="first name of coordinator")
    coordinator_lastname: str = Field(..., max_length=45, description="last name of coordinator")
    coordinator_middlename: Optional[str] = Field(None, max_length=45, description="middle name of coordinator")
    coordinator_phone: str = Field(..., max_length=20, description="phone number of coordinator")
    coordinator_address: str = Field(..., max_length=100, description="address of coordinator")
    marital_status: Marital_Status
    qualification:str = Field(..., max_length=255, description="qualification of student")
    lga: str = Field(..., max_length=255, description="lga of student")
    language_spoken: str
    riwaya: str
    category: str
    gender: Gender

    _val_firstname = uppercased("firstname")
    _val_lastname = uppercased("lastname")
    _val_middlename = uppercased("middlename")
    _val_address = uppercased("address")
   

class StudentCreate(BaseModel):
    marital_status: str
    qualification: str
    language_spoken:str
    riwaya: str
    category: str
    lga: str = Field(..., max_length=255, description="lga of student")
    coordinator_uuid: str = Field(..., description="unique id of coordinator")
    user_account_uuid: str = Field(..., description="uuid of user account")
    creator_uuid: str = Field(..., description="uuid of creator")


class StudentUpdate(BaseModel):
    lga: str = Field(..., max_length=255, description="lga of student")
    gender: Optional[Gender] = Field(None)
    marital_status: str
    qualification:str = Field(..., max_length=255, description="qualification of student")
    language_spoken: str
    riwaya: str
    category: str


class StudentFilter(BaseModel):
    phone: Optional[str] = Field(None, max_length=20)
    nin: Optional[str] = Field(None, max_length=16)
    marital_status: str
    qualification:str = Field(..., max_length=255, description="qualification of student")
    language_spoken:str = Field(..., max_length=255, description="image of student")
    riwaya:str = Field(..., max_length=255, description="image of student")
    lga: str = Field(..., max_length=255, description="lga of student")
    category: str


class StudentOut(BaseSchemaMixin):
    qualification:str = Field(..., max_length=255, description="qualification of student")
    language_spoken:str
    riwaya: str
    category: str
    lga: str = Field(..., max_length=255, description="lga of student")
    coordinator_uuid: str = Field(..., description="unique id of coordinator")
    user_account_uuid: str = Field(..., description="uuid of user account")
    creator_uuid: str = Field(..., description="uuid of creator")

    user_account: UserAccountOut
    coordinator: CoordinatorOut
    creator: UserMin


class StudentList(ListBase):
    result: List[StudentOut]