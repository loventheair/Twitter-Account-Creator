from fastapi import APIRouter, status, Response, Depends
from .. import schemas
import oauth2

router = APIRouter(tags=["Followers"], prefix="/followers")


@router.get("/", response_model=schemas.Engagments)
def get_followers(current_user=Depends(oauth2.get_current_user)):
    return  # return followers from database


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Engagments
)
def create_followers_camp(
    payload: schemas.FollowersCamp, current_user=Depends(oauth2.get_current_user)
):
    # insert the data into the database
    return  # the created followers campaign


@router.put("/{id}", response_model=schemas.Engagments)
def update_followers_camp(
    id: int,
    payload: schemas.UpdateFollowersCamp,
    current_user=Depends(oauth2.get_current_user),
):
    # update data in the db
    return  # the updated data


@router.delete("/{id}")
def delete_followers_camp(id: int, current_user=Depends(oauth2.get_current_user)):
    # delete data from db
    return Response(status_code=status.HTTP_200_OK)
