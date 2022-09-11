import time
from turtle import Turtle
from fastapi import APIRouter, Depends, status, Path, Query, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response
from sqlmodel import Session, select

from app import oauth2
from .. import models
import tweepy
import os
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from app.deps import get_db
from app.core.config import settings


android_mobiel_emulation = {
    "deviceName": "Nexus 5",
}
ios_mobile_emulation = {
    "deviceName": "iPhone X",
}


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])


router = APIRouter(tags=["App Auth"], prefix="/authorize-app")


@router.get("/")
async def first_step_auth(
    *,
    account_id: int = Path(title="path of the account to authorize", default=...),
    method: str = Query(default=..., title="web,android,ios"),
    request: Request
):
    global oauth1_user_handler
    global oauth2_user_handler
    global id_
    id_ = account_id
    global driver
    global account_method
    account_method = method
    # oauth2_user_handler = tweepy.OAuth2UserHandler(
    #     client_id=CLIENT_ID,
    #     redirect_uri=request.url_for("second_step_auth"),
    #     scope=["tweet.read", "tweet.write", "users.read"],
    #     client_secret=CLIENT_SECRET,
    # )
    oauth1_user_handler = tweepy.OAuth1UserHandler(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token=settings.access_token,
        access_token_secret=settings.access_token_secret,
        callback=request.url_for("second_step_auth"),
    )
    if method == "web":
        driver = webdriver.Chrome(
            options=chrome_options, executable_path=ChromeDriverManager().install()
        )
    elif method == "android":
        chrome_options.add_experimental_option(
            "mobileEmulation", android_mobiel_emulation
        )
        driver = webdriver.Chrome(
            options=chrome_options, executable_path=ChromeDriverManager().install()
        )

    elif method == "ios":
        chrome_options.add_experimental_option("mobileEmulation", ios_mobile_emulation)
        driver = webdriver.Chrome(
            options=chrome_options, executable_path=ChromeDriverManager().install()
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="invalid method"
        )
    driver.get(oauth1_user_handler.get_authorization_url())


@router.get("/second-step-auth")
async def second_step_auth(request: Request, session: Session = Depends(get_db)):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    access_token, access_token_secrete = oauth1_user_handler.get_access_token(
        request.query_params.get("oauth_verifier")
    )
    auth = tweepy.OAuthHandler(
        consumer_key=settings.consumer_key, consumer_secret=settings.consumer_secret
    )
    auth.set_access_token(access_token, access_token_secrete)
    api = tweepy.API(auth=auth)
    account_id = api.verify_credentials().id
    account_to_update = session.exec(
        select(models.Accounts).where(models.Accounts.id == id_)
    ).first()
    if account_method == "web":
        account_to_update.twitter_id = account_id
        account_to_update.web_access_token = access_token
        account_to_update.web_access_token_secret = access_token_secrete
        account_to_update.web_authorized = True
        session.add(account_to_update)
        session.commit()
    elif account_method == "android":
        account_to_update.twitter_id = account_id
        account_to_update.android_access_token = access_token
        account_to_update.android_access_token_secret = access_token_secrete
        account_to_update.android_authorized = True
        session.add(account_to_update)
        session.commit()
    elif account_method == "ios":
        account_to_update.twitter_id = account_id
        account_to_update.ios_access_token = access_token
        account_to_update.ios_access_token_secret = access_token_secrete
        account_to_update.ios_authorized = True
        session.add(account_to_update)
        session.commit()
    driver.close()
    return Response(
        content="successfuly authorized app",
        status_code=status.HTTP_200_OK,
    )
