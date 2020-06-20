from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import twitter_credentials

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import csv
import re


def clean_tweet(tweet):
    return " ".join(
        re.sub("(RT|@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()
    )


def analyze_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))

    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity == 0:
        return "Neutral"
    else:
        return "Negative"


class TwitterAuthenticator:
    def authenticate_twitter_app(self):
        auth = OAuthHandler(
            twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET
        )
        auth.set_access_token(
            twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET
        )
        return auth


class TwitterStreamer:
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            data = json.loads(data)
            if data["lang"] == "en":
                text = "'" + data["text"].replace("\n", " ") + "'"
                text = clean_tweet(data["text"])
                sentiment = analyze_sentiment(text)
                field = [
                    data["id"],
                    text,
                    data["user"]["location"],
                    data["place"],
                    sentiment,
                ]
                print(field)
                with open(fetched_tweets_filename, "a") as csvfile:
                    csvwriter = csv.writer(
                        csvfile, delimiter=",", quotechar="'", quoting=csv.QUOTE_ALL
                    )
                    # csvwriter.writerow(
                    #     ["twitter_id", "text", "location", "place", "sentiment"]
                    # )
                    csvwriter.writerow(field)
                return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer:
    """
    Functionality for analyzing and categorizing content from tweets.
    """


if __name__ == "__main__":

    hash_tag_list = ["covid", "coronavirus", "pandemic", "lockdown"]
    fetched_tweets_filename = "tweets.csv"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
