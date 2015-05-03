#!/usr/bin/env python

import os
from twython import Twython, TwythonError, TwythonStreamer
#import psycopg2
#import urlparse

# Possible future DB use? Save tweets / those blocked ... 
# DB init
# DB clear down
# delete from the_table where the_timestamp < now() - interval '30 days'

# Streaming class for Twython, infinite loop so all the work needs to be done from here!
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            # Print tweet to logs
            print data['text'].encode('utf-8')
            # Need to check is the tweet from the person being tracked, so a command? 
            print data 

    def on_error(self, status_code, data):
        print status_code
	# Add some alerting to the user here - email etc so they can restart the app in Heroku, if needed


if __name__ == '__main__':
	# Get details of the application you created as part of the bot process
	APP_KEY = os.getenv('APP_KEY')
        APP_SECRET = os.getenv('APP_SECRET')
        OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
        OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')
	# Get your Twitter id
	id_to_track = os.getenv('TWITTER_ID')
	
	print "Initialising personal block bot for: ",id_to_track
    
    # DB init
    # Read in current list of followers
    # Read in current list of blocks
    # Read in current list of mutes

	stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
	stream.statuses.filter(track=id_to_track)
