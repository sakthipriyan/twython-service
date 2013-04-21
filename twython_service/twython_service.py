'''
Created on 16-Apr-2013
@author: sakthipriyan
'''
import logging, urllib2, os, time, threading
from ConfigParser import RawConfigParser, NoSectionError, NoOptionError
from twython import Twython
from models import TwythonServiceError, Tweet
from database import Database

class TwythonService(object):
    def __init__(self, tweet_config, db_path, connect_time = 10):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        logging.debug('Twython Service: Initializing Twython Service')
        if(not os.path.isfile(tweet_config)):
            error_msg = 'Twython Service: Invalid twitter config file: ' + tweet_config
            logging.error(error_msg)
            raise TwythonServiceError(error_msg);
        try:
            config = RawConfigParser()
            config.read(tweet_config)
            self.__twitter = Twython(twitter_token = config.get('TweetAuth','twitter_token'),
                                   twitter_secret = config.get('TweetAuth','twitter_secret'),
                                   oauth_token = config.get('TweetAuth','oauth_token'),
                                   oauth_token_secret = config.get('TweetAuth','oauth_token_secret'))
            logging.debug('Twython Service: Loaded twitter configuration')    
            self.__wait_time = (1,2,4,8,16,32,64,128,64,32,16,8,4,2,1)
            self.__wait_index = -1
            self.__connect_time = connect_time
            self.__database = Database(db_path)
            self.__tweet_ready = threading.Event()
            self.__tweet_ready.set()
            self.__is_alive = True
            self.__process_thread = threading.Thread(target=self.__process_tweets)
            self.__process_thread.start()
        except NoSectionError, NoOptionError:
            error_msg = 'Twython Service: Twitter initialization failed'
            logging.debug(error_msg)
            raise TwythonServiceError(error_msg);
        
    def new_tweet(self, text, image_file = None, expires_in = 2592000):
        '''
        text is mandatory, image is optional.
        If tweet text is longer than 140, it is split into multiple tweets.
        tweet will expire in 30 if expiry_time is not specified.
        '''
        if not self.__is_alive:
            raise TwythonServiceError('Twython Service: Processor thread is terminated')
        expiry_ts = int(time.time()) + expires_in 
        if(len(text) < 140):
            logging.debug('Twython Service: Tweet < 140: '+ text)
            self.__database.insert_tweet(Tweet(text, image = image_file, expiry_ts = expiry_ts))
            self.__tweet_ready.set()
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
        no_of_tweets = str(len(output_array))
        logging.debug('Twython Service: Number of split up tweets '+ no_of_tweets)
        append_txt = '/' + no_of_tweets
        count = 0
        for text in output_array:
            count = count + 1
            tweet_txt = text + str(count) + append_txt
            logging.debug('Twython Service: Tweet > 140: '+ text)
            if(count == 1):
                tweet = Tweet(tweet_txt, image = image_file, expiry_ts = expiry_ts)
            else:
                tweet = Tweet(tweet_txt, expiry_ts = expiry_ts)
            self.__database.insert_tweet(tweet)
        self.__tweet_ready.set()

    def terminate(self):
        self.__is_alive = False
        self.__tweet_ready.set()
        
    def __wait_for_internet(self):
        connected = False
        while not connected:
            try:
                urllib2.urlopen('http://www.google.com', timeout = self.__connect_time)
                connected = True
            except Exception:
                self.__wait_index = self.__wait_index + 1
                if self.__wait_index == len(self.__wait_time):
                    self.__wait_index = 0
                sleep_time = self.__wait_time[self.__wait_index]
                logging.debug('No Internet: Sleeping for ' + str(sleep_time) + 's')
                time.sleep(sleep_time)
        return connected

    def __process_tweets(self):
        logging.debug('Twython Service: Processor thread to process tweets initialized')
        self.__database.delete_tweets()
        while self.__tweet_ready.wait() and self.__is_alive:
            logging.debug('Twython Service: Processing tweets')
            self.__tweet_ready.clear()
            tweet_id = 0
            while self.__wait_for_internet():
                tweet = self.__database.select_tweet(tweet_id) 
                if tweet is None:
                    logging.debug('Twython Service: No tweets to post')
                    break
                logging.debug('Twython Service: Sending tweet ' + str(tweet))
                try:
                    if tweet.image is None:
                        self.__twitter.updateStatus(status=tweet.text)
                        logging.debug('Twython Service: Tweet send')
                    else:
                        self.__twitter.updateStatusWithMedia(tweet.image,status=tweet.text)
                        logging.debug('Twython Service: Tweet send with an image')
                    tweet.expiry_ts = int(time.time())
                    self.__database.update_tweet(tweet)
                except Exception, e:
                    tweet_id = tweet.tweet_id
                    logging.error('Twython Service: ' + str(e))
                    time.sleep(10)
        logging.debug('Twython Service: Exiting processor thread')