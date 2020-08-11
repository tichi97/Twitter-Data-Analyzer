from twitterProject.models import TweetAnalyzer, TwitterClient
import numpy as np
import pandas as pd 


def tweets(username):
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweetAnalyzer = TweetAnalyzer()
    try:
        tweets = api.user_timeline(screen_name=username, count=100)
        # tweets = [tweetAnalyzer.clean_tweet(tweet) for tweet in totaltweets]
        df = tweetAnalyzer.tweets_to_data_frame(tweets)
        df['sentiment'] = np.array(
            [tweetAnalyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    except:
        df=pd.DataFrame() 
    return df


def trendTweets(topic):
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweetAnalyzer = TweetAnalyzer()
    topic = topic.split(" ")
    topic = "+".join(topic)
    tweets = tweetAnalyzer.filter_tweets(topic, "2019-01-01")

    df = tweetAnalyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array(
        [tweetAnalyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
    return df

