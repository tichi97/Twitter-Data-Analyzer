# allows you to listen to the tweets
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob


import os
import numpy as np
import pandas as pd
import re  
import matplotlib.pyplot as plt


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweets in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweets)
        return home_timeline_tweets


class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(os.environ.get('CONSUMER_KEY'),
                            os.environ.get('CONSUMER_SECRET'))
        auth.set_access_token(os.environ.get('ACCESS_TOKEN'),
                              os.environ.get('ACCESS_TOKEN_SECRET'))
        return auth


class TwitterStreamer():
    """
    CLass for streaming and processing live tweets
    """

    def __init__(self):
        self .twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweet_filename, hash_tag_list):
        # This hadnles twitter authentication and the connection to the twitter streaming api
        listener = TwitterListener(fetched_tweet_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # filter tweets
        stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):
    """
    basic listener class that prints receiveed tweets to stdout
    """
    # overriding classes

    def __init__(self, fetched_tweet_filename):
        self.fetched_tweet_filename = fetched_tweet_filename

    def on_data(self, data):  # takes in data from the listening
        try:
            print(data)
            with open(self.fetched_tweet_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def one_error(self, status):  # what happens if there is an error
        if status == 420:
            return False  # in case rate limit occurs
        print(status)  # status=error


class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """

    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.api = API(self.auth)

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:  # if its positive
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:  # tweet is negative
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(
            data=[tweet.text for tweet in tweets], columns=["tweets"])
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

    def filter_tweets(self, search_terms, date):
        tweets = []
        for tweet in Cursor(self.api.search, q=search_terms, lang="en", since=date).items(100):
            tweets.append(tweet)
        return tweets
