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
    
    def __str__(self):
        return u'Tweet[tweet_id=' + str(self.tweet_id) + ',text=' + str(self.text) + ',image=' + str(self.image) + ',expiry_ts=' + str(self.expiry_ts) + ']'

