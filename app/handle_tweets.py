import tweepy
from app.core.config import settings


def publish_tweet(access_token, access_token_secret, proxy, text: str, media: bytes):
    auth = tweepy.OAuthHandler(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    api = tweepy.API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, proxy=proxy
    )
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    res = api.update_status_with_media(status=text, file=media)
    return res.json()["data"]["id"]


def engage_with_like(access_token, access_token_secret, tweet_id: int, proxy):
    auth = tweepy.OAuthHandler(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    api = tweepy.API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, proxy=proxy
    )
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    api.create_favorite(tweet_id)


def engage_with_follow(access_token, access_token_secret, account_name_on_twitter: str):
    auth = tweepy.OAuthHandler(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    api.create_friendship(account_name_on_twitter)


def engag_with_reply(access_token, access_token_secret, tweet_id: int):
    auth = tweepy.OAuthHandler(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    api.update_status(
        status="your message here",
        in_reply_to_status_id=tweet_id,
        auto_populate_reply_metadata=True,
    )


def engag_quote(access_token, access_token_secret, tweet_id: int):
    auth = tweepy.OAuthHandler(
        consumer_key=settings.consumer_key,
        consumer_secret=settings.consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    api.retweet(id=tweet_id, trim_user=False)
