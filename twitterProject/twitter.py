from twitterProject.models import TweetAnalyzer, TwitterClient
import numpy as np


def tweets(username):
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()
    tweetAnalyzer = TweetAnalyzer()
    tweets = api.user_timeline(screen_name=username, count=100)
    # tweets = [tweetAnalyzer.clean_tweet(tweet) for tweet in totaltweets]
    df = tweetAnalyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array(
        [tweetAnalyzer.analyze_sentiment(tweet) for tweet in df['tweets']])
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


# def trendTweets(topic):
#     tweetAnalyzer = TweetAnalyzer()

#     topic = topic.split(" ")
#     topic = "+".join(topic)

#     tweets = tweetAnalyzer.filter_tweets(topic, "2019-01-01")
#     loc = []
#     txts = []
#     dates = []
#     for tweet in tweets:
#         txts.append(tweet.text)
#         dates.append(tweet.created_at)
#         if tweet.place:
#             loc.append(tweet.place.country)
#     return txts, loc, dates
