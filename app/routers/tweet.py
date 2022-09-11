from typing import Optional
from fastapi import (
    APIRouter,
    status,
    UploadFile,
    Form,
    Response,
    Depends,
    Query,
    HTTPException,
)
from .. import schemas, models, handle_tweets
import datetime
from sqlmodel import Session, select
from ..deps import get_db
from ..oauth2 import get_current_user
from typing import Union

router = APIRouter(tags=["Tweet"], prefix="/tweet")


@router.post(
    "/",
    response_model=schemas.CreateTweet,
    status_code=status.HTTP_201_CREATED,
)
def create_tweet(
    image: UploadFile,
    due_date: datetime.date = Form(default=...),
    language: str = Form(default=...),
    generated: bool = Form(default=False),
    # name: str = Form(default=...),
    content: str = Form(default=...),
    # collection: str = Form(default=...),
    # alt_text: str = Form(default=...),
    # type: str = Form(default=...),
    current_user=Depends(get_current_user),
    session: Session = Depends(get_db),
):
    # insert the image first
    asset_to_add = models.Assets(image_asset=image.file.read())
    session.add(asset_to_add)
    session.commit()
    # then insert the tweet
    tweet_to_add = models.Tweets(
        date=due_date,
        language=language,
        generated=generated,
        content=content,
        asset_id=asset_to_add.id,
        owner_id=current_user.id,
    )
    session.add(tweet_to_add)
    session.commit()
    session.refresh(tweet_to_add)
    return tweet_to_add


@router.put("/{id}", response_model=schemas.CreateTweet)
def update_tweet(
    id: int,
    image: UploadFile = None,
    # name: str = Form(default=None),
    language: str = Form(default=None),
    content: str = Form(default=None),
    generated: bool = Form(default=None),
    # collection: str = Form(default=None),
    # alt_text: str = Form(default=None),
    due_date: datetime.datetime = Form(default=None),
    session: Session = Depends(get_db)
    # type: str = Form(default=None),
):
    tweet_to_update = session.exec(
        select(models.Tweets).where(models.Tweets.id == id)
    ).first()
    if not tweet_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with {id=} was not found",
        )
    if language is not None:
        tweet_to_update.language = language
    if content is not None:
        tweet_to_update.content = content
    if generated is not None:
        tweet_to_update.generated = generated
    if due_date is not None:
        tweet_to_update.date = due_date
    if image is not None:
        # insert the asset first
        asset_to_update = session.exec(
            select(models.Assets).where(models.Assets.id == tweet_to_update.asset_id)
        ).first()
        asset_to_update.image_asset = image.file.read()
        session.add(asset_to_update)
        session.commit()
    session.add(tweet_to_update)
    session.commit()
    session.refresh(tweet_to_update)
    return tweet_to_update


@router.delete("/{id}")
def delete_tweet(
    id: int, session: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    tweet_to_delete = session.exec(
        select(models.Tweets).where(
            models.Tweets.id == id, models.Tweets.owner_id == current_user.id
        )
    ).first()
    if not tweet_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with {id=} was not found",
        )
    session.delete(tweet_to_delete)
    session.commit()
    return Response(status_code=status.HTTP_200_OK)


@router.get("/", response_model=Union[schemas.CreateTweet, list[schemas.CreateTweet]])
def get_one_or_many_tweets(
    id: int = Query(default=None),
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if id is not None:
        tweet = session.exec(
            select(models.Tweets).where(
                models.Tweets.id == id, models.Tweets.owner_id == current_user.id
            )
        ).first()
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"tweet with {id=} was not found",
            )

        return tweet
    tweet = session.exec(
        select(models.Tweets).where(models.Tweets.owner_id == current_user.id)
    ).all()
    return tweet


@router.post("/publish-tweet/{id}")
def publish_tweet(
    id: int,
    account_id: int = Query(default=...),
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    tweet_to_publish = session.exec(
        select(models.Tweets).where(
            models.Tweets.id == id, models.Tweets.owner_id == current_user.id
        )
    ).first()
    if not tweet_to_publish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"tweet with {id=} was not found",
        )
    account_to_publish_on = session.exec(
        select(models.Accounts).where(models.Accounts.id == account_id)
    ).first()
    account_proxy = session.exec(
        select(models.Proxy).where(models.Proxy.id == account_to_publish_on.proxy_id)
    ).first()
    if account_to_publish_on.web_authorized == True:
        tweet_id = handle_tweets.publish_tweet(
            access_token=account_to_publish_on.web_access_token,
            access_token_secret=account_to_publish_on.web_access_token_secret,
            proxy=f"https://{ account_proxy.username }:{ account_proxy.password }@{account_proxy.ip}:{account_proxy.proxy}",
        )
    if account_to_publish_on.android_authorized == True:
        tweet_id = handle_tweets.publish_tweet(
            access_token=account_to_publish_on.android_access_token,
            access_token_secret=account_to_publish_on.android_access_token_secret,
            proxy=f"https://{ account_proxy.username }:{ account_proxy.password }@{account_proxy.ip}:{account_proxy.proxy}",
        )

    if account_to_publish_on.ios_authorized == True:
        tweet_id = handle_tweets.publish_tweet(
            access_token=account_to_publish_on.ios_access_token,
            access_token_secret=account_to_publish_on.ios_access_token_secret,
            proxy=f"https://{ account_proxy.username }:{ account_proxy.password }@{account_proxy.ip}:{account_proxy.proxy}",
        )

    tweet_to_publish.generated = True
    tweet_to_publish.twitter_id = tweet_id
    session.commit()
    return Response(status_code=status.HTTP_200_OK)
