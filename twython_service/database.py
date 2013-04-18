'''
Created on 19-Apr-2013

@author: sakthipriyan
'''
import logging
import os
import sqlite3

create_tweets_table = '''CREATE TABLE "tweets" (
"tweet_id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"text" TEXT NOT NULL,
"image" TEXT,
"expiry_ts" INTEGER NOT NULL
);'''

insert_tweet = 'INSERT INTO tweets (text, image, expiry_ts) values(?,?,?)'


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
    
    def new_tweet(self,tweet):
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
            
