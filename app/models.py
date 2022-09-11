from optparse import Option
from sqlmodel import SQLModel, Field, LargeBinary, Column, ARRAY, Integer
from typing import Optional
import datetime

binary_type = LargeBinary()


class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    password: str = Field(unique=True)


class Accounts(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    twitter_id: int = Field(default=None, nullable=True)
    username: str = Field(unique=True)
    password: str = Field(unique=True)
    alt_email: str = Field(unique=True)
    alt_password: str = Field(unique=True)
    proxy_id: int = Field(foreign_key="proxy.id")
    user_id: int = Field(foreign_key="users.id")
    web_access_token: str = Field(default=None, nullable=True)
    web_access_token_secret: str = Field(default=None, nullable=True)
    android_access_token: str = Field(default=None, nullable=True)
    android_access_token_secret: str = Field(default=None, nullable=True)
    ios_access_token: str = Field(default=None, nullable=True)
    ios_access_token_secret: str = Field(default=None, nullable=True)
    web_authorized: bool = Field(default=False)
    android_authorized: bool = Field(default=False)
    ios_authorized: bool = Field(default=False)


class Proxy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    proxy: str
    ip: str
    username: str = Field(default=None, nullable=True)
    password: str = Field(default=None, nullable=True)


class Tweets(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    twitter_id: Optional[int] = Field(default=None, nullable=True)
    date: datetime.date
    language: str
    generated: bool
    content: str
    asset_id: int = Field(foreign_key="assets.id")
    owner_id: int = Field(foreign_key="users.id")


class Assets(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_asset: bytes = Field(sa_column=Column(LargeBinary))


class Engagments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    engag_type: str
    date: datetime.date
    amount: Optional[int] = Field(default=None, nullable=True)
    account_to_follow_id: Optional[int] = Field(default=None, nullable=True)
    engag_accounts_ids: Optional[list[int]] = Field(sa_column=Column(ARRAY(Integer)))
    owner_id: int = None
    random: Optional[bool] = Field(default=False, nullable=True)
