'''
Created on 19-Apr-2013

@author: sakthipriyan
'''
import logging
import os
import sqlite3
import time
from twython_service.models import Tweet

create_tweets_table = '''CREATE TABLE "tweets" (
"tweet_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"text" TEXT NOT NULL,
"image" TEXT,
"expiry_ts" INTEGER NOT NULL
);'''

insert_tweet = 'INSERT INTO tweets (text, image, expiry_ts) values(?,?,?)'
select_tweet = 'SELECT * FROM tweets where expire_ts > ? ORDER BY tweet_id LIMIT 1'
update_tweet = 'UPDATE tweets set expire_ts = ? where tweet_id = ?'
delete_tweet = 'DELETE FROM tweets where expiry_ts < ?'

class Database(object):
    def __init__(self, db_file):
        self.db_file = db_file
        if(not os.path.isfile(db_file)):
            connection = None
            try:
                connection = sqlite3.connect(self.db_file)
                cursor = connection.cursor()
                cursor.execute(create_tweets_table)
            except sqlite3.Error, e:
                logging.error("Error %s:" % e.args[0])
            finally:
                if connection:
                    connection.close()
    
    def insert_tweet(self,tweet):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(insert_tweet,(tweet.text,tweet.image,tweet.expiry_ts))
            connection.commit()
        except sqlite3.Error, e:
            logging.error("Error %s:" % e.args[0])
        finally:
            if connection:
                connection.close()
    
    def select_tweet(self):
        connection = None
        tweet = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(select_tweet,(int(time.time()),))
            data = cursor.fetchone()
            if data:
                tweet = Tweet(data[1], data[0], data[2], data[3])
        except sqlite3.Error, e:
            logging.error("Error %s:" % e.args[0])
        finally:
            if connection:
                connection.close()
        return tweet
        
    def update_tweet(self, tweet):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(update_tweet,(tweet.expiry_ts,tweet.tweet_id))
            connection.commit()
        except sqlite3.Error, e:
            logging.error("Error %s:" % e.args[0])
        finally:
            if connection:
                connection.close()
    
    def delete_tweets(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            cursor.execute(delete_tweet,(int(time.time()),))
            connection.commit()
        except sqlite3.Error, e:
            logging.error("Error %s:" % e.args[0])
        finally:
            if connection:
                connection.close()
