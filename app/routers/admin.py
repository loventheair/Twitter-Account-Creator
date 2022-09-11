from fastapi import APIRouter, status
from .. import schemas

router = APIRouter(tags=["Admin"])


@router.post("/service")
def add_service(payload):
    # todo date to be recieved
    ...
