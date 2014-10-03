import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import sys
import json
import os


#Change working directory
os.chdir('<set your working directory>')


# Consumer keys and access tokens, used for OAuth
consumer_key = '<add your consumer_key>'
consumer_secret ='<add your consumer_key>'
access_token = '<add your access_token>'
access_token_secret = '<add your access_token_secret>'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

file = open('tweety.json', 'a')

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_data(self, data):
        json_data = json.loads(data)
        file.write(str(json_data))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['bike'])
#search for location and keyword:
#api.filter(locations=[103.60998,1.25752,104.03295,1.44973], track=['twitter'])

