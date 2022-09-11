from fastapi import (
    APIRouter,
    Response,
    status,
    UploadFile,
    Form,
    Depends,
    HTTPException,
    Query,
)
from app import oauth2
from .. import schemas, models
from ..deps import get_db
from sqlmodel import Session, select
import random
from typing import Union

router = APIRouter(tags=["Accounts"], prefix="/accounts")


@router.get("/", response_model=Union[schemas.AccountOut, list[schemas.AccountOut]])
def get_accounts(
    id: int = Query(default=None),
    current_user: schemas.TokenData = Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    if id is not None:
        account = session.exec(
            select(models.Accounts).where(
                models.Accounts.id == id, models.Accounts.user_id == current_user.id
            )
        ).first()
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"account with {id=} was not found",
            )
        return account
    accounts = session.exec(
        select(models.Accounts).where(current_user.id == models.Accounts.user_id)
    ).all()
    return accounts


# @router.post("/", response_model=schemas.Account)
# def create_account(
#     profile_picture: UploadFile,
#     cover_picture: UploadFile,
#     profile_picture_rand=Form(default=...),
#     profiel_picture_rand=Form(default=...),
#     name: str = Form(default=...),
#     country: str = Form(default=...),
#     pirvacy: str = Form(default=...),
#     bio: str = Form(default=...),
#     bio_random: bool = Form(default=...),
#     amount: int = Form(default=...),
#     current_user=Depends(oauth2.get_current_user),
# ):
# inesrt the data into the database
# return  # the created data from database


@router.post("/add/one", response_model=schemas.Account)
def add_account(
    proxy: UploadFile,
    username: str = Form(default=...),
    password: str = Form(default=...),
    alt_email_or_phone: str = Form(default=...),
    alt_password: str = Form(default=...),
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    proxy_schema = {
        "ip": None,
        "proxy": None,
        "username": None,
        "password": None,
    }
    proxy_to_add = models.Proxy(
        **dict(
            zip(
                proxy_schema,
                [
                    input.removesuffix("\r\n")
                    for input in proxy.file.readline().decode().split(":")
                ],
            )
        )
    )

    session.add(proxy_to_add)
    session.commit()

    account_to_add = models.Accounts(
        username=username,
        password=password,
        alt_email=alt_email_or_phone,
        alt_password=alt_password,
        proxy_id=proxy_to_add.id,
        user_id=current_user.id,
    )
    session.add(account_to_add)

    session.commit()
    session.refresh(account_to_add)
    return account_to_add


@router.post("/add/multible")
def add_accounts(
    login_credentials: UploadFile,
    proxies: UploadFile,
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    proxy_schema = {
        "ip": None,
        "proxy": None,
        "username": None,
        "password": None,
    }
    login_creds_schema = {
        "username": None,
        "password": None,
        "alt_email": None,
        "alt_password": None,
    }
    inserted_proxies_ids = []
    for line in proxies.file.readlines():
        proxy_obj = models.Proxy(
            **dict(
                zip(
                    proxy_schema,
                    [input.removesuffix("\r\n") for input in line.decode().split(":")],
                )
            )
        )
        session.add(proxy_obj)
        session.commit()
        inserted_proxies_ids.append(proxy_obj.id)

    for line in login_credentials.file.readlines():
        login_obj = models.Accounts(
            **dict(
                zip(
                    login_creds_schema,
                    [input.removesuffix("\r\n") for input in line.decode().split(":")],
                )
            )
        )
        login_obj.proxy_id = random.choice(inserted_proxies_ids)
        login_obj.user_id = current_user.id
        session.add(login_obj)
    session.commit()

    return {"Success": "Accounts created successfuly"}


@router.put("/{id}", response_model=schemas.Account)
def update_account(
    id: int,
    # profile_picture: UploadFile | None = None,
    # cover_picture: UploadFile | None = None,
    # profile_picture_rand: bool = Form(default=None),
    # profiel_picture_rand: bool = Form(default=None),
    # name: str = Form(default=None),
    # country: str = Form(default=None),
    # pirvacy: str = Form(default=None),
    # bio: str = Form(default=None),
    # bio_random: bool = Form(default=None),
    # amount: int = Form(default=None),
    # current_user=Depends(oauth2.get_current_user),
    update_data: schemas.UpdateAccount,
    session: Session = Depends(get_db),
):

    account_to_update = session.exec(
        select(models.Accounts).where(models.Accounts.id == id)
    ).first()

    for attribute, value in update_data.dict(exclude_none=True).items():
        setattr(account_to_update, attribute, value)
    session.add(account_to_update)
    session.commit()
    session.refresh(account_to_update)
    return account_to_update


@router.delete("/{id}")
def delete_account(
    id: int,
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    account_to_delete = session.exec(
        select(models.Accounts).where(models.Accounts.id == id)
    ).first()
    if account_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="UnAuthorized Action"
        )

    session.delete(account_to_delete)
    session.commit()
    return Response(status_code=status.HTTP_200_OK)
