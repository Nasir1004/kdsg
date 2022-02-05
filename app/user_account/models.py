#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-09-20 09:39:38
# @Author  : Nasiru Ibrahim Abba
# @Description : something cool


from sqlalchemy import Column, ForeignKey, String, Enum, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Date
from datetime import date

from app.config.database import Base
from app.mixins.columns import BaseMixin


class NextOfKin(BaseMixin, Base):
    firstname = Column(String(length=45), nullable=False)
    lastname = Column(String(length=45), nullable=False)
    middlename = Column(String(length=45), nullable=True, default="")
    phone = Column(String(length=20), nullable=False)
    address = Column(String(length=255), nullable=False, default="")


class Coordinator(BaseMixin, Base):
    firstname = Column(String(length=45), nullable=False)
    lastname = Column(String(length=45), nullable=False)
    middlename = Column(String(length=45), nullable=True, default="")
    phone = Column(String(length=20), nullable=False)
    address = Column(String(length=255), nullable=False, default="")

    students: relationship = relationship("Student", back_populates="coordinator")


class UserAccount(BaseMixin, Base):
    user_uuid = Column(String(length=50), ForeignKey('users.uuid', onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    nin = Column(String(length=16), ForeignKey("nins.nin"), nullable=True, unique=True)
    image = Column(String(length=255), nullable=False)
    phone = Column(String(length=20), nullable=False)
    address = Column(String(length=255), nullable=False, default="")
    gender = Column(Enum("m", "f", "na", name="gender_type_2"), nullable=False)
    birthdate = Column(Date, nullable=False)
    next_of_kin_uuid = Column(String(length=50), ForeignKey("nextofkins.uuid"), nullable=True)
    creator_uuid = Column(String(length=50), ForeignKey("users.uuid"), nullable=False)

    user: relationship = relationship("User", lazy="joined", foreign_keys=[user_uuid])
    creator: relationship = relationship("User", lazy="joined", foreign_keys=[creator_uuid])


class Student(BaseMixin, Base):
    user_account_uuid = Column(String(length=50), ForeignKey("useraccounts.uuid"), nullable=False)
    registration_date = Column(Date, nullable=False, default=date.today(), server_default=func.current_date())
    marital_status = Column(Enum("single","married"), name ="marital_status", default="single", nullable=False)
    qualification = Column(String(length=255), nullable=False)
    lga = Column(String(length=255), nullable=False)
    language_spoken = Column(Enum("housa", "yoruba", 'igbo', "english", default="housa", nullable=False))
    riwaya = Column(Enum("hafs", "warsh", "qalun", "al_duri", "khallad", " Khalaf ", "shuab", "ibn_amir", "hisham", "thakwan",  "albuzze", "qumbul", "as_sosee", name="riwaya_type", default="hafs"), nullable=False)
    category = Column(Enum("sixty_hizbs_tafsir", "sixty_Hizbs", "fourty_Hizbs", "twenty_Hizbs", "ten_hizbs_and_tangeem", "two_Hizbs",  name="category_type"), nullable=False)
    creator_uuid = Column(String(length=50), ForeignKey("users.uuid"), nullable=False)
    coordinator_uuid = Column(String(length=50), ForeignKey('coordinators.uuid'), nullable=True)

    coordinator: relationship = relationship("Coordinator", lazy="joined", back_populates="students")
    user_account: relationship = relationship("UserAccount", lazy="joined", foreign_keys=[user_account_uuid])
    creator: relationship = relationship("User", lazy="joined")