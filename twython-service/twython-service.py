'''
Created on 16-Apr-2013

@author: sakthipriyan
'''
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
from twython import Twython
import logging
import urllib2
import os
import time

class TwythonServiceError(Exception):
    pass

class Tweet(object):
    def __init__(self, tweet, id = 0, image = None, expiry_ts = 0):
        self.id = id;
        self.tweet = tweet
        self.image = image
        self.expiry_ts = expiry_ts
    
class TwythonService(object):
    def __init__(self, tweet_config, connect_time = 15, db_path = None):
        if(not os.path.isfile(tweet_config)):
            raise TwythonServiceError('Invalid twitter config file: ' + tweet_config);
        try:
            config = RawConfigParser()
            config.read(tweet_config)
            self.twitter = Twython(twitter_token = config.get('TweetAuth','twitter_token'),
                                   twitter_secret = config.get('TweetAuth','twitter_secret'),
                                   oauth_token = config.get('TweetAuth','oauth_token'),
                                   oauth_token_secret = config.get('TweetAuth','oauth_token_secret'))
            self.wait_time = (1,2,4,8,16,32,64,128,64,32,16,8,4,2,1)
            self.wait_index = -1
            self.connect_time = connect_time
            self.db_path = db_path
            self.tweet_queue = Queue()
        except NoSectionError, NoOptionError:
            raise TwythonServiceError('Twitter initialization failed');
            
    def new_tweet(self, text, image_file = None, expiry_time = 0):
        
        if(len(text) <= 140):
            enqueue_tweet(text, image_file, expiry_time)
            return
        
        split_array = text.split(' ')
        output_array = []
        output = u''
        for text in split_array:
            if len(output + text) < 135:
                output = output + text + ' '
            else:
                output_array.append(output)
                output = text + ' '
        output_array.append(output)
        
        append_txt = '/' + str(len(output_array))
        count = 0
        for text in output_array:
            count = count + 1
            tweet = text + str(count) + append_txt
            if(count == 1):
                enqueue_tweet(Tweet(text, image = image_file, expiry_ts = 0))
            else:
                enqueue_tweet(Tweet(text, expiry_ts = 0))
            
    def wait_for_internet(self):
        connected = False
        while not connected:
            try:
                urllib2.urlopen('http://www.google.com',timeout = self.connect_time)
                connected = True
            except Exception:
                self.wait_index = self.wait_index + 1
                if self.wait_index == len(self.wait_time):
                    self.wait_index = 0
                time.sleep(self.wait_time[self.wait_index])
                
    def enqueue_tweet(self, tweet):
        print 'tweet added'
        
    def dequeue_tweet(self):
        print 'tweet removed'

    def process_tweets(self):
        while True:
            wait_for_internet()
            try:
                pass
                #self.twitter.updateStatus(status=text)
            except Exception, e:
                pass
