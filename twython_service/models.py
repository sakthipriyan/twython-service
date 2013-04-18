'''
Created on 19-Apr-2013

@author: sakthipriyan
'''

class TwythonServiceError(Exception):
    pass

class Tweet(object):
    def __init__(self, text, tweet_id = 0, image = None, expiry_ts = 0):
        self.tweet_id = tweet_id;
        self.text = text
        self.image = image
        self.expiry_ts = expiry_ts
