from fastapi import APIRouter, Response, status, Form, UploadFile, Depends
from .. import schemas, oauth2

router = APIRouter(tags=["Profiles"], prefix="/profiles")


@router.get("/", response_model=schemas.Profile)
def get_profiles(current_user=Depends(oauth2.get_current_user)):
    # get profiels from db
    return


@router.post("/", response_model=schemas.Profile)
def create_profile(
    profile_picture: UploadFile,
    cover_picture: UploadFile,
    name: str = Form(default=...),
    coutnry: str = Form(default=...),
    privacy: str = Form(default=...),
    profile_picture_rand: bool = Form(default=...),
    cover_picture_rand: bool = Form(default=...),
    bio: str = Form(default=...),
    current_user=Depends(oauth2.get_current_user),
):
    # insert data into db
    return  # return created data


# @router.put("/profiles/{id}")
# def edit_profile(
#     id: int,
#     profile_picture: UploadFile | None = None,
#     cover_picture: UploadFile | None = None,
#     name: str = Form(default=None),
#     coutnry: str = Form(default=None),
#     privacy: str = Form(default=None),
#     profile_picture_rand: bool = Form(default=None),
#     cover_picture_rand: bool = Form(default=None),
#     bio: str = Form(default=None),
#     current_user=Depends(oauth2.get_current_user),
# ):
#     # updated the data in db
#     return  # the updated data


@router.delete("/{id}")
def delete_profile(id: int, current_user=Depends(oauth2.get_current_user)):
    # delete data from db
    return Response(status_code=status.HTTP_200_OK)
