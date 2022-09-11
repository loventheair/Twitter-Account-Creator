from webbrowser import get
from fastapi import APIRouter, Query, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, oauth2
from ..deps import get_db
from sqlmodel import Session, select
from .. import models, utils

router = APIRouter(tags=["login"])


@router.post(
    "/email-us",
    response_model=schemas.ReturnRequest,
)
def send_request(payload: schemas.SendRequest):
    # send the request data to the database
    return payload  # then return the successfuly inserted data to the response


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
def sign_up(
    payload: models.Users,
    session: Session = Depends(get_db),
):
    payload.password = utils.hash(payload.password)
    session.add(payload)
    session.commit()
    access_token = oauth2.gen_token({"sub": str(payload.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/sign-in")
def sign_in(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db),
):
    user_data = session.exec(
        select(models.Users).where(
            models.Users.email == user_credentials.username,
        )
    ).first()
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )

    access_token = oauth2.gen_token({"sub": str(user_data.id)})
    return {"access_token": access_token, "token_type": "bearer"}
