'''
Created on 16-Apr-2013

@author: sakthipriyan
'''
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
from twython import Twython
from twythonservice.models import Tweet
import logging
import urllib2
import os
import time

    
class TwythonService(object):
    def __init__(self, tweet_config, db_path, connect_time = 15):
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
        except NoSectionError, NoOptionError:
            raise TwythonServiceError('Twitter initialization failed');
            
    def new_tweet(self, text, image_file = None, expiry_time = 0):
        '''
        text is mandatory, image is optional.
        tweet will expire in 30 if expiry_time is not specified.
        '''
        expiry_ts = int(time.time()) 
        expiry_ts = expiry_ts + expiry_time if expiry_time != 0 else 2592000 
        if(len(text) <= 140):
            enqueue_tweet(Tweet(text, image = image_file, expiry_ts = expiry_ts))
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
                enqueue_tweet(Tweet(text, image = image_file, expiry_ts = expiry_ts))
            else:
                enqueue_tweet(Tweet(text, expiry_ts = expiry_ts))
            
    def wait_for_internet(self):
        connected = False
        while not connected:
            try:
                urllib2.urlopen('http://www.google.com', timeout = self.connect_time)
                connected = True
            except Exception:
                self.wait_index = self.wait_index + 1
                if self.wait_index == len(self.wait_time):
                    self.wait_index = 0
                time.sleep(self.wait_time[self.wait_index])
        return connected
                
    def enqueue_tweet(self, tweet):
        print 'tweet added'
        
    def dequeue_tweet(self):
        print 'tweet removed'

    def process_tweets(self):
        while self.wait_for_internet():
            try:
                tweet = self.dequeue_tweet()
                if tweet.image is None:
                    self.twitter.updateStatus(status=tweet.tweet)
                else:
                    self.twitter.updateStatusWithMedia(tweet.image,status=tweet.tweet)
            except Exception, e:
                self.enqueue_tweet(tweet)

