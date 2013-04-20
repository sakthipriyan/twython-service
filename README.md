Twython Service
===============
Twython Service adds another level of abstraction while posting tweets via Twython.

## Using Twython Service in code
`````python
# To initialize the TwythonService object
#tweet_config = path to tweet config file
#db_path = path to store the sqlite db used by the twython service
twython_service = TwythonService(tweet_config, db_path)

# To insert new tweet
#tweet_text = text to be tweeted out. It is mandatory field.
#image_to_attach = Optional field. Path to image file which will be attached to the tweet.
#expiry_time = Time limit to post the tweet. Optional field, defaults to 30 days.
twython_service.new_tweet(text=tweet_text, image_file = image_to_attach, expiry_time = expiry_time)

`````
