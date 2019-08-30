# allows you to listen to the tweets
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from textblob import TextBlob

import twitter_credentials
import numpy as np
import pandas as pd
import re  # regular expression
import matplotlib.pyplot as plt

import copy


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
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCESS_TOKEN_SECRET)
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
        tweets = stream.filter(track=hash_tag_list)
        return tweets


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

    def on_error(self, status):  # what happens if there is an error
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
        tweets = Cursor(self.api.search, q=search_terms,
                        lang="en", since=date).items(150)
        return tweets


if __name__ == "__main__":
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweetAnalyzer = TweetAnalyzer()
    # tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)
    # print(dir(tweets[0])) #what we can extract from the tweets
    # print(tweets[0].retweets)
    tweets = tweetAnalyzer.filter_tweets("vma -filter:retweets", "2019-01-01")
    loc = []
    txts = []
    dates = []
    for tweet in tweets:
        txts.append(tweet.text)
        dates.append((tweet.created_at.month, tweet.created_at.day))
        if tweet.place:
            loc.append(tweet.place.country)

    # print(txts)
    number_of_tweets = len(txts)
    print(number_of_tweets)
    print(loc)
    print(dates)
    print(type(dates[1]))
    # x = loc
    # loc = ["US", "Kenya", "US", "UG", "Kenya", "Haiti", "US",
    # "Kenya", "US", "TZ", "TZ", "US", "RW", "US", "TZ", ]
    objects = set(loc)
    y_pos = np.arange(len(objects))
    performance = []
    countries = {}
    for country in objects:
        num = loc.count(country)
        # countries[country] = num
        performance.append(num)

    countries
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel('Number of Tweets')
    plt.title('Number of Tweets per Country')

    plt.show()

    plt.hist(dates, bins=6)
    plt.xlabel('Dates')
    plt.title('Number of Tweets')
    plt.show()
    ######################################################################################
    # df = tweetAnalyzer.tweets_to_data_frame(tweets)
    # df['sentiment'] = np.array(
    #     [tweetAnalyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    # print(df.head(10))
    #############################################################################################

    # labels = ['Negative', 'Positive', 'Neutral']
    # neg = len([v for v in df['sentiment'] if v == -1])
    # pos = len([v for v in df['sentiment'] if v == 1])
    # nt = len([v for v in df['sentiment'] if v == 0])
    # sizes = [neg, pos, nt]
    # colors = ['red', 'blue', 'grey']
    # explode = (0, 0.1, 0)  # explode 1st slice

    # # Plot
    # plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    #         autopct='%1.1f%%', shadow=True, startangle=140)

    # plt.axis('equal')
    # plt.show()
    #############################################################################################

    # objects = ('Negative', 'Positive')
    # y_pos = np.arange(len(objects))
    # performance = [neg, pos]

    # plt.bar(y_pos, performance, align='center', alpha=0.5)
    # plt.xticks(y_pos, objects)
    # plt.ylabel('Number of Tweets')
    # plt.title('Positive Tweets vs Negative Tweets')

    # plt.show()

    ##################################################################################

    # # get average length of all tweets
    # print(np.mean(df['len']))

    # # get number of likes for the most liked tweet
    # print(np.max(df['likes']))

    # # number of retweets for the most retweeted tweet
    # print(np.max(df['retweets']))

    # # Time series
    # # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # # time_likes.plot(figsize=(16, 4), color='r')
    # # plt.show()

    # # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # # time_retweets.plot(figsize=(16, 4), color='r')
    # # plt.show()

    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16, 4), label='likes', legend=True)

    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16, 4), label='retweets', legend=True)
    # plt.show()

    # # print(df.head(10))

    #########################################################################################

    # hash_tag_list = ['donald trump', 'hilary clinton',
    #                  'barack obama', 'bernie sanders']
    # fetched_tweet_filename = "tweets.json"
    # twitter_client = TwitterClient('jackieaina')
    # # print(twitter_client.get_user_timeline_tweets(1))
    # twitter_streamer = TwitterStreamer()
    # tweets = twitter_streamer.stream_tweets(
    #     fetched_tweet_filename, hash_tag_list)
