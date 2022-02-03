#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-10 11:04:57
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


import json
from typing import Optional, Union
from app.user.schemas import UserCreate
from app.utils.misc import gen_email, gen_random_password
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException
import requests
from app.nin.schemas import NINCreate, NINSchema


load_dotenv()


def get_nin_from_store(nin: str, token: str) -> dict:
    url: str = getenv("NIN_STORE_URL", default="") + nin
    header = {"Authorization": f"Bearer {token}"}
    response: requests.Response = requests.get(url, headers=header)
    
    if response.status_code > 299:
        try:
            raise HTTPException(response.status_code, detail=response.json()["detail"])
        except json.decoder.JSONDecodeError:
            raise HTTPException(403, detail="Could not retrieve NIN, Invalid response or NIN not found")

    indigene_data: dict = response.json()
    return indigene_data


def gen_nin_from_dict(nin_data: dict, user_id):
    data_to_update = nin_data.copy()
    data_to_update["image"] = nin_data["photo"]
    data_to_update["address"] = nin_data["residence"]["address1"]
    data_to_update["pulled_by"] = user_id

    nin_model = NINCreate(**data_to_update)
    return nin_model


def gen_user_from_nin(nin_info: NINSchema):
    user_dict = {"email": gen_email(nin_info.nin), "password": gen_random_password(), "firstname": nin_info.firstname,\
        "lastname": nin_info.lastname, "middlename": nin_info.middlename}
    
    return UserCreate(**user_dict)