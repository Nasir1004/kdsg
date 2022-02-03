#!/usr/bin/env python
# -=-<[ Bismillahirrahmanirrahim ]>-=-
# -*- coding: utf-8 -*-
# @Date    : 2021-05-24 00:40:54
# @Author  : Dahir Muhammad Dahir
# @Description : something cool


from app.utils.custom_validators import currency_out_val
from enum import Enum
from typing import Any, List, Optional


from app.mixins.schemas import BaseSchemaMainMixin, BaseSchemaMixin
from pydantic import BaseModel, Field, EmailStr, validator
from datetime import date


class Gender(str, Enum):
    male = "m"
    female = "f"
    na = "NA"


class WalletStatus(str, Enum):
    enabled = "enabled"
    disabled = "disabled"
    closed = "closed"


class WalletTxnType(str, Enum):
    credit = "credit"
    debit = "debit"


class PaymentAccountStatus(str, Enum):
    activated = "activated"
    deactivated = "deactivated"
    blacklisted = "blacklisted"


class EnrollmentStatus(str, Enum):
    enrolled = "enrolled"
    not_enrolled = "not_enrolled"


class VehicleStatus(str, Enum):
    not_activated = "not_activated"
    activated = "activated"
    deactivated = "deactivated"
    blacklisted = "blacklisted"


class NINImageOut(BaseModel):
    nin: str = Field(..., max_length=16)
    image: str = Field(..., max_length=160)

    class Config:
        orm_mode = True


class UserOut(BaseSchemaMixin):
    email: EmailStr
    firstname: str
    lastname: str
    middlename: Optional[str] = ''
    is_active: bool
    is_system_user: bool

    class Config:
        orm_mode = True


class VehicleQROut(BaseModel):
    qr_file: str

    class Config:
        orm_mode = True


class DateRange(BaseModel):
    column_name: str
    from_date: date
    to_date: date


class ListBase(BaseModel):
    count: int
    sum_total: Optional[float] = Field(None)

    _val_sum = currency_out_val("sum_total")


class LoanTypeMin(BaseSchemaMixin):
    name: str = Field(..., max_length=100, min_length=3, description="Loan Type Name")
    min_payment_amount: float = Field(..., gt=0, description="Minimum Payment Amount")
    total_loan_amount: float = Field(..., gt=0, description="Total Loan Amount")
    loan_payment_cycle: int = Field(..., gt=0, \
        description="Loan Payment Cycle in days, e.g 1 for daily, 7 for weekly e.t.c")
    loan_payment_duration: int = Field(..., gt=0, \
        description="Loan Payment Duration in days, e.g 365 for 1 year, 30 for 1 month e.t.c")
    min_num_of_beneficiaries: int = Field(..., gt=0, description="Minimum Number of Beneficiaries")
    max_num_of_beneficiaries: int = Field(..., gt=0, description="Maximum Number of Beneficiaries")

    _val_min_payment_amt = currency_out_val("min_payment_amount")
    _val_total_loan_amt = currency_out_val("total_loan_amount")



class SubUnitMin(BaseSchemaMixin):
    name: str = Field(..., max_length=45, description="Sub Unit Name")
    display_name: Optional[str] = Field(None, max_length=45, description="Sub Unit Display Name")
    unit_uuid: str = Field(..., description="Unit UUID")

class UnitMin(BaseSchemaMixin):
    unit_name: str = Field(..., max_length=45, description="Unit Name")
    unit_code: str = Field(..., max_length=45, description="Unit Code")
    local_government_uuid: str = Field(..., description="Local Government UUID")
    loan_type_uuid: str = Field(..., description="Loan Type UUID")


class OrganizationMin(BaseSchemaMixin):
    name: str = Field(..., max_length=100, description="Organization Name")
    display_name: Optional[str] = Field(None, max_length=100, description="Organization Display Name")
    contact_number: str = Field(..., max_length=20, description="Organization Contact Number")


class AssociationMin(BaseSchemaMixin):
    name: str = Field(..., max_length=100, description="Association Name")
    contact_number: str = Field(..., max_length=20, description="Association Contact Number")
    organization_uuid: str = Field(..., description="Organization UUID")
    loan_type_uuid: str = Field(..., description="Loan Type UUID")


class UserMin(BaseSchemaMixin):
    email: EmailStr
    firstname: str
    lastname: str
    middlename: Optional[str] = ''


class UserMinPublic(BaseSchemaMainMixin):
    firstname: str
    lastname: str
    middlename: Optional[str] = ''


class LocalGovernmentMin(BaseSchemaMainMixin):
    name: str = Field(..., max_length=45)
    display_name: str = Field(..., max_length=100)


class LoanBeneficiaryMin(BaseSchemaMixin):
    user_account_uuid: str = Field(..., description="uuid of user account")
    loan_type_uuid: str = Field(..., description="uuid of vehicle type")
    vehicle_id: str = Field(..., max_length=45, description="system generated id of vehicle")
    association_number: str = Field(..., max_length=45, description="Association number of Beneficiary")
    creator_uuid: str = Field(..., description="uuid of creator")


class UserAccountMin(BaseSchemaMixin):
    user_uuid: str = Field(..., description="unique id of user")
    next_of_kin_uuid: Optional[str] = Field(None, description="unique id of next of kin")
    nin: Optional[str] = Field(None, max_length=16, description="nin of user")
    image: str = Field(..., max_length=255, description="image of user")
    phone: str = Field(..., max_length=20, description="Phone number of the user")
    address: str = Field(..., description="address of user")
    gender: Gender
    birthdate: date

    user: UserMin


class UserAccountMinPublic(BaseSchemaMainMixin):
    user: UserMinPublic


class UserAccountPhone(BaseModel):
    phone: str = Field(..., max_length=20, description="Phone number of the user")

    class Config:
        orm_mode = True


class GuarantorMin(BaseSchemaMixin):
    firstname: str = Field(..., max_length=45, description="first name of guarantor")
    lastname: str = Field(..., max_length=45, description="last name of guarantor")
    middlename: Optional[str] = Field(None, max_length=45, description="middle name of guarantor")
    phone: str = Field(..., max_length=20, description="phone number of guarantor")
    address: str = Field(..., max_length=100, description="address of guarantor")


class WalletMin(BaseSchemaMixin):
    id: int = Field(None)
    wallet_number: int = Field(..., description="Wallet number")
    owner_uuid: str = Field(..., description="Owner uuid")
    super_wallet_owner_uuid: Optional[str] = Field(None, description="Super wallet owner uuid")
    balance: float = Field(..., description="Wallet balance")
    status: WalletStatus = Field(..., description="Wallet status")

    _balance_val = currency_out_val("balance")


class SuperWalletOwnerMin(BaseSchemaMixin):
    display_name: str = Field(..., description="Display name")
    user_uuid: str = Field(..., description="User uuid")


class WalletTxnMin(BaseSchemaMixin):
    wallet_number: int = Field(..., description="Wallet number")
    type: WalletTxnType = Field(..., description="Transaction type")
    amount: float = Field(..., description="Amount")
    performed_by: str = Field(..., description="Performed by uuid")

    _val_amount = currency_out_val("amount")


class LoanPaymentAccountMin(BaseSchemaMixin):
    loan_payer_uuid: str = Field(..., max_length=45, description="Loan Payer UUID")
    loaned_item_id: str = Field(..., max_length=45, description="Loaned Item ID")
    loan_type_uuid: str = Field(..., max_length=45, description="Loan Type UUID")
    paid_till_date: Optional[date] = Field(None, description="Paid Till Date")
    status: Optional[PaymentAccountStatus] = Field(None, description="Payment Account Status")


class LoanPaymentTxnMin(BaseSchemaMixin):
    loaned_item_id: str = Field(..., max_length=45, description="Loaned Item ID")
    amount: float = Field(..., gt=0, description="Amount")
    days_paid: int = Field(..., ge=1, description="Days Paid")
    txn_id: str = Field(..., max_length=45, description="Transaction ID")
    txn_receipt: str = Field(..., max_length=100, description="Transaction Receipt")
    wallet_txn_uuid: str = Field(..., max_length=45, description="Wallet Transaction UUID")
    loan_type_uuid: str = Field(..., max_length=45, description="Loan Type UUID")
    txn_date: Optional[date] = Field(None, description="Transaction Date")
    performed_by: str = Field(..., max_length=45, description="Performed By")

    _val_amount = currency_out_val("amount")


class LoanPaymentStakeHolderMin(BaseSchemaMixin):
    name: str = Field(..., max_length=45, description="Stake Holder Name")


class LoanPaymentStakeMin(BaseSchemaMixin):
    stake_holder: str = Field(..., max_length=100, description="Stake Holder Name")
    stake_name: str = Field(..., max_length=100, description="Stake Name")
    stake_amount: float = Field(..., description="Stake Amount")
    loan_type_name: Optional[str] = Field(None, max_length=100, description="Loan Type Name")

    _val_stake_amount = currency_out_val("stake_amount")


class LoanPaymentBreakdownMin(BaseSchemaMixin):
    stake_holder: str = Field(..., max_length=100)
    stake_name: str = Field(..., max_length=100)
    amount: float = Field(...)
    loan_payment_txn_uuid: str = Field(...)
    txn_date: date = Field(..., description="Transaction Date")
    performed_by: str = Field(..., max_length=45, description="Performed By")

    _val_amount = currency_out_val("amount")


class VehicleMin(BaseSchemaMixin):
    vehicle_type_uuid: str = Field(..., description="Vehicle Type UUID")
    chassis_number: str = Field(..., min_length=6, max_length=17, description="Chassis Number")
    engine_number: str = Field(..., max_length=24, description="Engine Number")
    tracking_id: Optional[str] = Field(None, max_length=45, description="Tracking Number")
    color: str = Field(..., max_length=45, description="Color")
    vehicle_id: str = Field(..., max_length=45, description="Vehicle ID")
    vehicle_subunit_uuid: str = Field(..., description="Vehicle Subunit UUID")
    creator_uuid: str = Field(..., description="Creator UUID")
    qr_code_image: str = Field(..., max_length=255, description="QR Code Image")
    unique_key: str = Field(..., description="Unique Key")
    status: VehicleStatus = Field(VehicleStatus.not_activated, description="Status")


class UnitFull(UnitMin):
    loan_type: LoanTypeMin
    sub_units: List[SubUnitMin]
    local_government: LocalGovernmentMin


class SubUnitFull(SubUnitMin):
    unit: UnitMin


class LocalGovernmentFull(LocalGovernmentMin):
    units: List[UnitFull]


class OrganizationFull(OrganizationMin):
    associations: List[AssociationMin]


class AssociationFull(AssociationMin):
    organization: OrganizationMin
    loan_type: LoanTypeMin


class UserAccountFull(UserAccountMin):
    user: UserMin


class LoanBeneficiaryMid(LoanBeneficiaryMin):
    user_account: UserAccountMin


class LoanBeneficiaryPublic(BaseModel):
    user_account: UserAccountMinPublic

    class Config:
        orm_mode = True

class LoanBeneficiaryFull(LoanBeneficiaryMin):
    user_account: UserAccountMin
    vehicle_type: LoanTypeMin
    vehicle: VehicleMin
    creator: UserMin


class WalletFull(WalletMin):
    owner: UserMin
    super_wallet_owner: Optional[SuperWalletOwnerMin]


class SuperWalletOwnerFull(SuperWalletOwnerMin):
    user: UserMin
    wallets: List[WalletMin]


class WalletTxnFull(WalletTxnMin):
    wallet: WalletFull
    performer: UserMin


class LoanPaymentAccountFull(LoanPaymentAccountMin):
    loan_payment_txns: List[LoanPaymentTxnMin]
    loan_payer: UserAccountMin


class LoanPaymentTxnVendor(LoanPaymentTxnMin):
    performer: UserMin
    loan_payment_account: LoanPaymentAccountMin
    loan_type: LoanTypeMin


class LoanPaymentTxnFull(LoanPaymentTxnMin):
    performer: UserMin
    loan_payment_account: LoanPaymentAccountMin
    wallet_txn: WalletTxnMin
    loan_type: LoanTypeMin
    loan_payment_breakdowns: List[LoanPaymentBreakdownMin]


class StakeHolderFull(LoanPaymentStakeHolderMin):
    pass


class LoanPaymentStakeFull(LoanPaymentStakeMin):
    loan_type: LoanTypeMin


class LoanPaymentBreakdownFull(LoanPaymentBreakdownMin):
    loan_payment_txn: LoanPaymentTxnMin
    loan_payment_stake: LoanPaymentStakeMin

