from datetime import date
from optparse import Option
import requests
from pydantic import BaseModel, validator, ValidationError, EmailStr
from email_validator import validate_email
from .core.config import settings
from sqlmodel import SQLModel
from typing import Optional


class Content(BaseModel):
    id: int
    name: str
    step: int  # ? int or str
    collection: str
    due_date: date
    published: bool
    last_modified: date


class Assets(Content):
    pass


class EngagmentsOut(BaseModel):
    id: int
    engag_type: str
    # language: str
    # engag_c: list[int]
    date: date
    amount: int
    engag_accounts_ids: list[int]
    random: bool
    owner_id: int


class CreateEngagments(SQLModel):
    engag_type: str
    # account_id: int
    # language: str
    engag_accounts_ids: list[int]
    date: date
    amount: int
    random: bool


class UpdateEnagments(BaseModel):
    engag_type: Optional[str] = None
    # account_id: int | None = None
    language: Optional[str] = None
    engag_accounts: Optional[list[int]] = None
    date: Optional[date] = None
    amount: Optional[int] = None
    random: Optional[bool] = None


class CreateTweet(BaseModel):
    id: int
    # name: str
    language: str
    generated: bool
    content: str
    # collection: str
    # alt_text: str
    date: date
    # type: str
    owner_id: int


class MessageCamp(BaseModel):
    id: int
    type: str
    language: str
    due_date: date
    recievers: list[str]
    sender_accounts: list[str]
    random: bool
    amount: int
    text: str


class UpdateMessageCamp(BaseModel):
    type: Optional[str] = None
    language: Optional[str] = None
    due_date: Optional[date] = None
    recievers: Optional[list[str]] = None
    sender_accounts: Optional[list[str]] = None
    random: Optional[bool] = None
    amount: Optional[int] = None
    text: Optional[str] = None


class FollowersCamp(BaseModel):
    id: int
    type: str
    language: str
    due_date: date
    account: list[str]
    engagments_accounts: list[str]
    random: bool
    amount: int


# class UpdateFollowersCamp(BaseModel):
#     type: str | None = None
#     language: str | None = None
#     due_date: date | None = None
#     account: list[str] | None = None
#     engagments_accounts: list[str] | None = None
#     random: bool | None = None
#     amount: int | None = None


class Account(BaseModel):
    id: int
    username: str
    password: str
    alt_email: str
    alt_password: str
    proxy_id: int
    user_id: int


class Profile(BaseModel):
    id: int
    name: str
    coutnry: str
    privacy: str
    bio: str


class ReturnFollowersCamp(FollowersCamp):
    id: int


class SendRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    message: str

    @validator("email")
    def email_validate(cls, value):
        if validate_email(email=value):
            return value
        else:
            raise ValidationError("Invalid Email")

    @validator("phone_number")
    def validate_phone_number(cls, value):

        res = requests.get(
            f"https://phonevalidation.abstractapi.com/v1/?api_key={settings.phone_verify_api_key}&phone={value}"
        )
        if res.json()["valid"] == True:
            return value
        else:
            raise ValueError("Invalid Phone Number")


# ? uuid or int
class ReturnRequest(SendRequest):
    request_id: int


class SignUp(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    # conf_password: str

    # @validator("conf_password")
    # def validate_password(cls, field_value, values, field, config):
    #     if field_value == values["password"]:
    #         return field_value

    #     else:
    #         raise ValueError("passwords don't match")


# ? uuid or int
class ReturnSignUp(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class SignIn(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: int


class Asset(BaseModel):
    name: str
    language: str
    collection: str
    alt_text: str
    due_date: date
    type: str


class AccountOut(SQLModel):
    id: int
    username: str
    password: str
    alt_email: str
    alt_password: str
    proxy_id: int
    user_id: int


class AddProxyOut(SQLModel):
    id: int
    proxy: str
    ip: str


class UpdateAccount(SQLModel):
    username: Optional[str] = None
    password: Optional[str] = None
    alt_email: Optional[str] = None
    alt_password: Optional[str] = None


class UpdateAccountReturn(SQLModel):
    id: int
    username: str
    alt_email: str
    proxy_id: int
    user_id: int
