import re
import tweepy
import os
from textblob import TextBlob

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def main():
    bearer_token = os.getenv('TWITTER')
    query = input("Please type the keyword you'd like to analyse:\n")
    api = tweepy.Client(bearer_token)
    tweets = []
    fetched_tweets = api.search_recent_tweets(query=query, max_results=100)

    if fetched_tweets.data != None:
        for tweet in fetched_tweets.data:
            # print(tweet.text)
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        print("Positive tweets percentage: {} %".format(round(100*len(ptweets)/len(tweets),1)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        print("Negative tweets percentage: {} %".format(round(100*len(ntweets)/len(tweets),1)))
        # percentage of neutral tweets
        print("Neutral tweets percentage: {} % \
            ".format(round(100*(len(tweets) -(len(ntweets)+len(ptweets)))/len(tweets),1)))

        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in ptweets[:5]:
            print("- " + tweet['text'])

        # printing first 5 negative tweets
        print("\n\nNegative tweets:")
        for tweet in ntweets[:5]:
            print("- " + tweet['text'])
    else:
        print("I'm sorry there's not enough results!")

if __name__ == "__main__":
	main()