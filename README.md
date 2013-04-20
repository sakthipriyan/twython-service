# Twython Service
Twython Service adds another level of abstraction while posting tweets via Twython.
It smoothly works over unstable Internet connection.  

## Installing Twython service
`````shell
# Installing Twython Service
git clone https://github.com/spriyan/twython-service.git
cd twython-service
sudo python setup.py install
`````

## Using Twython Service in code
`````python
# Initializing the TwythonService object
twython_service = TwythonService('/path/to/config/file','/path/to/database/file')

# Example of sending tweet
twython_service.new_tweet(text = 'Your tweet goes in here')

# Example of sending the tweet within specified time. Defaults to 30 days.
twython_service.new_tweet(text = 'Your tweet goes in here', expires_in=300)

# Example of sending the tweet with image 
twython_service.new_tweet(text = 'Your tweet goes in here', image_file='/path/to/image/file')

# Terminate the Twython Service 
twython_service.terminate()
`````
