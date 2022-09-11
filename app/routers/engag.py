from os import access
from fastapi import APIRouter, status, Response, Depends, Query, HTTPException

from app import handle_tweets
from .. import schemas, oauth2
from ..deps import get_db
from sqlmodel import Session, select
from .. import models
import tweepy
import random
from app.core.config import settings
from typing import Union


router = APIRouter(tags=["Engagments"], prefix="/engagments")


@router.get(
    "/", response_model=Union[schemas.EngagmentsOut, list[schemas.EngagmentsOut]]
)
def get_engag(
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
    id: int = Query(default=None),
):
    if id is not None:
        engagments_campaign = session.exec(
            select(models.Engagments).where(
                models.Engagments.id == id,
                models.Engagments.owner_id == current_user.id,
            )
        ).first()
        return engagments_campaign

    all_engagments = session.exec(
        select(models.Engagments).where(models.Engagments.owner_id == current_user.id)
    ).all()
    return all_engagments


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.EngagmentsOut
)
def add_engag(
    payload: models.Engagments,
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    payload.owner_id = current_user.id
    # print(current_user.id)
    session.add(payload)
    session.commit()
    session.refresh(payload)
    return payload


@router.put("/{id}", response_model=schemas.EngagmentsOut)
def update_engag(
    paylod: schemas.UpdateEnagments,
    id: int,
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    engag_to_update = session.exec(
        select(models.Engagments).where(models.Engagments.id == id)
    ).first()
    if not engag_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"engagment with {id=} was not found ",
        )
    # engag_to_update = models.Engagments(**paylod.dict(exclude_unset=True))
    for attr, value in paylod.dict(exclude_unset=True).items():
        setattr(engag_to_update, attr, value)
    # print(engag_to_update)
    session.add(engag_to_update)
    session.commit()
    session.refresh(engag_to_update)
    return engag_to_update


@router.delete("/{id}")
def delete_engag(
    id: int,
    current_user=Depends(oauth2.get_current_user),
    session: Session = Depends(get_db),
):
    engag_to_delete = session.exec(
        select(models.Engagments).where(
            models.Engagments.id == id, models.Engagments.owner_id == current_user.id
        )
    ).first()
    if not engag_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"engagments with id {id=} was not found",
        )
    session.delete(engag_to_delete)
    session.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/initiate-engagment/")
def initiate_engag(
    engag_id: int = Query(default=...),
    account_to_engag_on_id=Query(default=None),
    tweet_id=Query(default=None),
    session: Session = Depends(get_db),
    current_user=Depends(oauth2.get_current_user),
):

    user_accounts = session.exec(
        select(models.Accounts).where(
            models.Accounts.user_id == current_user.id,
            models.Accounts.id != account_to_engag_on_id,
        )
    ).all()
    engagment = session.exec(
        select(models.Engagments).where(
            models.Engagments.id == engag_id,
            models.Engagments.owner_id == current_user.id,
        )
    ).first()
    # engagment with like
    if engagment.engag_type == "like":
        if engagment.random == True:
            accounts: list[user_accounts] = random.sample(
                user_accounts, engagment.amount
            )
            for account in accounts:
                proxy = session.exec(
                    select(models.Proxy).where(models.Proxy.id == account.proxy_id)
                ).first()
                try:
                    if account.web_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                        )
                except:
                    continue
                try:
                    if account.android_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.android_access_token,
                            access_token_secret=account.android_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                        )
                except:
                    continue
                try:
                    if account.ios_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.ios_access_token,
                            access_token_secret=account.ios_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                        )
                except:
                    continue
        if engagment.random == False:
            engagment_accounts = session.exec(
                select(models.Accounts).where(
                    models.Accounts.id in engagment.engag_accounts_ids
                )
            ).all()
            for account in engagment_accounts:
                try:
                    if account.web_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                        )
                except:
                    continue
                try:
                    if account.android_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.android_access_token,
                            access_token_secret=account.android_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                        )
                except:
                    continue
                try:
                    if account.ios_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.ios_access_token,
                            access_token_secret=account.ios_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                        )
                except:
                    continue

    # engagment with follow
    if engagment.engag_type == "follow":
        account_to_follow = session.exec(
            select(models.Accounts).where(models.Accounts.id == account_to_engag_on_id)
        ).first()
        account_to_follow_name = tweepy.OAuthHandler(
            consumer_key=settings.consumer_key,
            consumer_secret=settings.consumer_secret,
            access_token=account_to_follow.web_access_token,
            access_token_secret=account_to_follow.web_access_token_secret,
        )
        api = tweepy.API(auth=account_to_follow_name)
        account_to_follow_name = api.verify_credentials()["name"]
        if engagment.random == True:
            accounts: list[user_accounts] = random.sample(
                user_accounts, engagment.amount
            )
            for account in accounts:
                proxy = session.exec(
                    select(models.Proxy).where(models.Proxy.id == account.proxy_id)
                ).first()
                try:
                    if account.web_authorized == True:
                        handle_tweets.engage_with_follow(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            account_name_on_twitter=account_to_follow_name,
                        )
                except:
                    pass
                try:
                    if account.android_authorized == True:
                        handle_tweets.engage_with_follow(
                            access_token=account.android_access_token,
                            access_token_secret=account.android_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            account_name_on_twitter=account_to_follow_name,
                        )
                except:
                    pass
                try:
                    if account.ios_authorized == True:
                        handle_tweets.engage_with_follow(
                            access_token=account.ios_access_token,
                            access_token_secret=account.ios_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            account_name_on_twitter=account_to_follow_name,
                        )
                except:
                    pass
        if engagment.random == False:
            engagment_accounts = session.exec(
                select(models.Accounts).where(
                    models.Accounts.id in engagment.engag_accounts_ids
                )
            ).all()
            for account in engagment_accounts:
                try:
                    if account.web_authorized == True:
                        handle_tweets.engage_with_follow(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            account_name_on_twitter=account_to_follow_name,
                        )
                except:
                    pass
                try:
                    if account.android_authorized == True:
                        handle_tweets.engage_with_follow(
                            access_token=account.android_access_token,
                            access_token_secret=account.android_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            account_name_on_twitter=account_to_follow_name,
                        )
                except:
                    pass
                try:
                    if account.ios_authorized == True:
                        handle_tweets.engage_with_like(
                            access_token=account.ios_access_token,
                            access_token_secret=account.ios_access_token_secret,
                            tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            account_name_on_twitter=account_to_follow_name,
                        )
                except:
                    pass

    if engagment.engag_type == "reply":

        tweet_to_reply = session.exec(
            select(models.Tweets).where(models.Tweets.id == tweet_id)
        ).first()
        # account_to_engage = session.exec(
        #     select(models.Engagments).where(models.Engagments.id == engag_id)
        # )
        # account_to_engage = tweepy.OAuthHandler(
        #     consumer_key=settings.consumer_key,
        #     consumer_secret=settings.consumer_secret,
        #     access_token=account_to_engage.web_access_token,
        #     access_token_secret=account_to_engage.web_access_token_secret,
        # )
        # api = tweepy.API(auth=account_to_follow_name)
        # account_to_follow_name = api.verify_credentials()["name"]
        if engagment.random == True:
            accounts: list[user_accounts] = random.sample(
                user_accounts, engagment.amount
            )
            for account in accounts:
                proxy = session.exec(
                    select(models.Proxy).where(models.Proxy.id == account.proxy_id)
                ).first()
                try:
                    if account.web_authorized == True:
                        handle_tweets.engag_with_reply(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            tweet_id=tweet_to_reply.twitter_id,
                        )
                except:
                    pass
                # try:
                #     if account.android_authorized == True:
                #         handle_tweets.engage_with_follow(
                #             access_token=account.android_access_token,
                #             access_token_secret=account.android_access_token_secret,
                #             tweet_id=tweet_id,
                #             proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                #             account_name_on_twitter=account_to_follow_name,
                #         )
                # except:
                #     pass
                # try:
                #     if account.ios_authorized == True:
                #         handle_tweets.engage_with_follow(
                #             access_token=account.ios_access_token,
                #             access_token_secret=account.ios_access_token_secret,
                #             tweet_id=tweet_id,
                #             proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                #             account_name_on_twitter=account_to_follow_name,
                #         )
                # except:
                #     pass
        if engagment.random == False:
            engagment_accounts = session.exec(
                select(models.Accounts).where(
                    models.Accounts.id in engagment.engag_accounts_ids
                )
            ).all()
            for account in engagment_accounts:
                try:
                    if account.web_authorized == True:
                        handle_tweets.engage_with_follow(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            # tweet_id=tweet_id,
                            proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            tweet_id=tweet_to_reply.twitter_id,
                        )
                except:
                    pass
                # try:
                #     if account.android_authorized == True:
                #         handle_tweets.engage_with_follow(
                #             access_token=account.android_access_token,
                #             access_token_secret=account.android_access_token_secret,
                #             tweet_id=tweet_id,
                #             proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                #             account_name_on_twitter=account_to_follow_name,
                #         )
                # except:
                #     pass
                # try:
                #     if account.ios_authorized == True:
                #         handle_tweets.engage_with_like(
                #             access_token=account.ios_access_token,
                #             access_token_secret=account.ios_access_token_secret,
                #             tweet_id=tweet_id,
                #             proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                #             account_name_on_twitter=account_to_follow_name,
                #         )
                # except:
                #     pass
    if engagment.engag_type == "reply_with_quote":
        tweet_to_retweet = session.exec(
            select(models.Tweets).where(models.Tweets.id == tweet_id)
        ).first()
        if engagment.random == True:
            accounts: list[user_accounts] = random.sample(
                user_accounts, engagment.amount
            )
            for account in accounts:
                proxy = session.exec(
                    select(models.Proxy).where(models.Proxy.id == account.proxy_id)
                ).first()
                try:
                    if account.web_authorized == True:
                        handle_tweets.engag_quote(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            # proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            tweet_id=tweet_to_retweet.twitter_id,
                        )
                except:
                    print("exception has occured")
        if engagment.random == False:
            engagment_accounts = session.exec(
                select(models.Accounts).where(
                    models.Accounts.id in engagment.engag_accounts_ids
                )
            ).all()
            for account in engagment_accounts:
                try:
                    if account.web_authorized == True:
                        handle_tweets.engag_quote(
                            access_token=account.web_access_token,
                            access_token_secret=account.web_access_token_secret,
                            # tweet_id=tweet_id,
                            # proxy=f"https://{proxy.username}:{proxy.password}@{proxy.ip}:{proxy.proxy}",
                            tweet_id=tweet_to_retweet.twitter_id,
                        )
                except:
                    print("exception has occured")
