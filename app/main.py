from fastapi import FastAPI
from .routers import (
    auth,
    tweet,
    engag,
    messages,
    profiles,
    asset,
    accounts,
    authorize_app,
)

from .models import *
from .database import create_tabls, database_create

database_create()
create_tabls()

app = FastAPI(title="Twitter Account Creator")
app.include_router(auth.router)
# app.include_router(details.router)
app.include_router(tweet.router)
app.include_router(engag.router)
# app.include_router(messages.router)
# app.include_router(profiles.router)
# app.include_router(asset.router)
app.include_router(accounts.router)
app.include_router(authorize_app.router)


@app.get("/")
def route():
    return {"message": "Hello World"}
