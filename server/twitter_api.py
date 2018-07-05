# Author Dalin Akrasi
# Student no.1528923
#
#
#
#

from tweepy import Stream, OAuthHandler, API
from tweepy.streaming import StreamListener
import json


CONSUMER_KEY =  "qropumbc8QqtAPvLN9kFMIrOB"
CONSUMER_SECRET = "aN9S0wFFoFPO1wuFn0ybMao4ovmVYnCfvrEUujO53doHUYDYMQ"
ACCESS_TOKEN = "157632547-Pslz3MLe0oGiyMKzPoWtc6dV53vBoaN4B87Wu6tn"
ACCESS_SECRET = "iHbrc9ZRyYg7haKC9WdkOj3Ed5T1NjxaOhgvbefIbA900"


class streamListener(StreamListener):
    def on_data(self, data):
        print data
        return True

    def on_error():
        print status



# tw_auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# tw_auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
# twitter = API(tw_auth)
# twitterSearch = twitter.search('#LivingKCL', tweet_mode='extended')
# twitterStream = Stream(tw_auth, streamListener())
# twitterStream.filter(track=["#LivingKCL"])
localData = json.load(open('tweez2.json'))



def getData():
    return twitterSearch


def getLocalData():
    return localData


def getTweets():
    return [{"text":tweet.full_text, "id":tweet.id, "date":tweet.created_at} for tweet in twitterSearch]

def getTweet(index):
    return {"text":twitterSearch[index].full_text, "id":twitterSearch[index].id, "date":twitterSearch[index].created_at}
