import tweepy
from django.conf import settings


class Twitter:
    def __init__(self):
        auth = tweepy.OAuthHandler(
            settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY
        )
        auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET
        )
        self.api = tweepy.API(auth)

    def post(self, tweet: str):
        self.api.update_status(tweet)
