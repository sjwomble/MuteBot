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
            print "id_to_track=",id_to_track
            ttwython.send_direct_message(screen_name=id_to_track, text=data['text'].encode('utf-8'))

    def on_error(self, status_code, data):
        print status_code
	# Add some alerting to the user here - email etc so they can restart the app in Heroku, if needed? Should restart itself... 


if __name__ == '__main__':
    # Get details of the application you created as part of the bot process
    APP_KEY = os.getenv('APP_KEY') 
    APP_SECRET = os.getenv('APP_SECRET')
    OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')
    # Get your Twitter id
    id_to_track = os.getenv('TWITTER_ID')
	
    print "Initialising personal block bot for: ",id_to_track
        
    # twitter object for sending DMs / muting / blocking
    ttwython = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    stream.statuses.filter(track=id_to_track)


#EXAMPLE DATA ->> 
#{u'in_reply_to_status_id_str': None, u'coordinates': None, u'in_reply_to_user_id': 3119097305, u'text': u'@sjwomble hello!', u'id': 594971352794292224, u'possibly_sensitive': False, u'retweet_count': 0, u'place': None, u'in_reply_to_user_id_str': u'3119097305', u'in_reply_to_screen_name': u'sjwomble', u'user': {u'is_translator': False, u'description': u'Cisgender Social Justice Womble. He/His. I follow back and I delete old tweets, hence the low number :)', u'profile_background_image_url_https': u'https://abs.twimg.com/images/themes/theme13/bg.gif', u'profile_use_background_image': True, u'listed_count': 5, u'profile_sidebar_fill_color': u'FFFFFF', u'default_profile_image': False, u'id': 3119097305, u'geo_enabled': False, u'followers_count': 4515, u'verified': False, u'profile_sidebar_border_color': u'EEEEEE', u'statuses_count': 461, u'notifications': None, u'url': u'http://sjwomble.wordpress.com', u'profile_link_color': u'93A644', u'screen_name': u'sjwomble', u'friends_count': 4577, u'location': u'Wimbledon Common', u'default_profile': False, u'profile_background_image_url': u'http://abs.twimg.com/images/themes/theme13/bg.gif', u'name': u'SJWomble', u'profile_background_color': u'B2DFDA', u'follow_request_sent': None, u'profile_banner_url': u'https://pbs.twimg.com/profile_banners/3119097305/1427387233', u'profile_text_color': u'333333', u'contributors_enabled': False, u'favourites_count': 205, u'profile_image_url': u'http://pbs.twimg.com/profile_images/581130376757821441/WuTfty_h_normal.jpg', u'protected': False, u'following': None, u'utc_offset': 3600, u'profile_image_url_https': u'https://pbs.twimg.com/profile_images/581130376757821441/WuTfty_h_normal.jpg', u'profile_background_tile': False, u'created_at': u'Thu Mar 26 16:20:03 +0000 2015', u'id_str': u'3119097305', u'lang': u'en-gb', u'time_zone': u'Dublin'}, u'truncated': False, u'source': u'<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', u'retweeted': False, u'in_reply_to_status_id': None, u'geo': None, u'entities': {u'user_mentions': [{u'name': u'SJWomble', u'id_str': u'3119097305', u'id': 3119097305, u'screen_name': u'sjwomble', u'indices': [0, 9]}], u'hashtags': [], u'trends': [], u'symbols': [], u'urls': []}, u'favorite_count': 0, u'filter_level': u'low', u'timestamp_ms': u'1430687199196', u'favorited': False, u'created_at': u'Sun May 03 21:06:39 +0000 2015', u'id_str': u'594971352794292224', u'contributors': None, u'lang': u'en'}
