from fastapi import APIRouter, status, UploadFile, Form, Response, Depends
from .. import schemas, oauth2
import datetime
from typing import Optional

router = APIRouter(tags=["Assets"], prefix="/asset")


@router.get("/", response_model=schemas.Assets)
def get_assets(current_user=Depends(oauth2.get_current_user)):
    return  # return assets data from the database


@router.post("/", response_model=schemas.Asset, status_code=status.HTTP_201_CREATED)
def create_asset(  # data will be uploaded in form data
    file: UploadFile,
    name: str = Form(default=...),
    language: str = Form(default=...),
    collection: str = Form(default=...),
    alt_text: str = Form(default=...),
    due_date: datetime.date = Form(default=...),
    type: str = Form(default=...),
    current_user=Depends(oauth2.get_current_user),
):
    # insert the data into the database
    return  # then return the inserted data back into the response


@router.put("/{id}", response_model=schemas.Asset)
def update_asset(
    file: Optional[UploadFile] = None,
    name: str = Form(default=None),
    language: str = Form(default=None),
    collection: str = Form(default=None),
    alt_text: str = Form(default=None),
    due_date: datetime.date = Form(default=None),
    type: str = Form(default=None),
    current_user=Depends(oauth2.get_current_user),
):
    # update the data in db
    return  # the updated data


@router.delete("/{id}")
def delete_asset(id: int, current_user=Depends(oauth2.get_current_user)):
    # delete from db
    return Response(status_code=status.HTTP_200_OK)
