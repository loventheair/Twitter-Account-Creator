from fastapi import APIRouter, status, Response, Depends
from .. import schemas, oauth2

router = APIRouter(tags=["Messages"], prefix="/messages")


@router.get("/", response_model=schemas.EngagmentsOut)
def get_messages(current_user=Depends(oauth2.get_current_user)):
    return  # return messages from databse


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.EngagmentsOut
)
def create_messages_campaign(
    payload: schemas.MessageCamp, current_user=Depends(oauth2.get_current_user)
):
    # insert the data into the database
    return  # return the created campaign


@router.put("/{id}", response_model=schemas.EngagmentsOut)
def update_messages_campaign(
    id: int,
    payload: schemas.UpdateMessageCamp,
    current_user=Depends(oauth2.get_current_user),
):
    # update the message in the db
    return  # the updated data


@router.delete("/{id}")
def delete_messages(id: int, current_user=Depends(oauth2.get_current_user)):
    # delete the data in the db
    return Response(status_code=status.HTTP_200_OK)
