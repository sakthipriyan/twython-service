'''
Created on 16-Apr-2013

@author: sakthipriyan
'''
import logging, urllib2, os, time, threading
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
from twython import Twython
from twython_service.models import Tweet, TwythonServiceError
from twython_service.database import Database
    
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
            self.database = Database(db_path)
            self.tweet_ready = threading.Event()
            self.tweet_ready.set()
            self.process_thread = threading.Thread(target=self.process_tweets)
            self.process_thread.start()
        except NoSectionError, NoOptionError:
            raise TwythonServiceError('Twitter initialization failed');
            
    def new_tweet(self, text, image_file = None, expiry_time = 0):
        '''
        text is mandatory, image is optional.
        If tweet text is longer than 140, it is split into multiple tweets.
        tweet will expire in 30 if expiry_time is not specified.
        '''
        expiry_ts = int(time.time()) 
        expiry_ts = expiry_ts + expiry_time if expiry_time != 0 else 2592000 
        if(len(text) < 140):
            self.database.insert_tweet(Tweet(text, image = image_file, expiry_ts = expiry_ts))
            self.tweet_ready.set()
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
                tweet = Tweet(text, image = image_file, expiry_ts = expiry_ts)
            else:
                tweet = Tweet(text, expiry_ts = expiry_ts)
            self.database.insert_tweet(tweet)
        self.tweet_ready.set()
            
            
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

    def process_tweets(self):
        while self.tweet_ready.is_set():
            self.tweet_ready.clear()
            while self.wait_for_internet():
                next_tweet = self.database.select_tweet() 
                if next_tweet is None: 
                    break
                try:
                    if tweet.image is None:
                        self.twitter.updateStatus(status=tweet.text)
                    else:
                        self.twitter.updateStatusWithMedia(tweet.image,status=tweet.text)
                except Exception, e:
                    pass

