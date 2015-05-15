#!/usr/bin/env python

import os
import time
from twython import Twython, TwythonError, TwythonStreamer
#import psycopg2
#import urlparse

# Possible future DB use? Save tweets / those blocked ... 
# DB init
# DB clear down
# delete from the_table where the_timestamp < now() - interval '30 days'
    
# Start timer
start_time = time.time()
ids_blocked = []
ids_muted = []

# Streaming class for Twython, infinite loop so all the work needs to be done from here!
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            # Print tweet to logs
            print data['text'].encode('utf-8')
            # Need to check is the tweet from the person being tracked and @'ing themselves, so a command? 
            if data['text'].startswith("@"+id_to_track) & data['user']['screen_name'].startswith(id_to_track):
                # is a connand message
                handleCommand(data['text'])
            else: 
                # Potential person to block
                handleTweet(data)

    def on_error(self, status_code, data):
        print "ERROR: ",status_code
	# Add some alerting to the user here - email etc so they can restart the app in Heroku, if needed? Should restart itself... 

# Commands include : (Only works when you @ yourself, so not likely to be triggered by accidenct!) 
#    PersonalBotOff (Won't mute or block any more
#    PersonalBotMute (Will start muting, on by default)
#    PersonalBotBlock (Will start blocking instead)
def handleCommand(tweet):
    print "Received a command ... ", tweet
    if "PersonalBotOff" in tweet:
        os.environ["MUTE_BLOCK_OFF"] = "off"
    if "PersonalBotMute" in tweet:
        os.environ["MUTE_BLOCK_OFF"] = "mute"
    if "PersonalBotBlock" in tweet:
        os.environ["MUTE_BLOCK_OFF"] = "block"
                
def handleTweet(tweet_json):
    print "Potential tweet to handle",tweet_json['text']
    # Only get friends list every 10 mins or it will seriously slow down blocking any dogpiles etc...
    global my_friends
    my_friends = getFriends(my_friends)
    #If friend then do nothing, otherwise block or mute (Or nothing if bot is off
    if tweet_json['user']['id_str'] not in my_friends:  
        mute_block_off = os.getenv('MUTE_BLOCK_OFF')
        msg = ""
        if mute_block_off == "block":
            if tweet_json['user']['id_str'] not in ids_blocked:  
                ttwython.create_block(user_id=tweet_json['user']['id_str'])
                # Not ideal as it will only track from start. TODO: put ids blocked by bot into a DB table
                global ids_blocked
                ids_blocked.append(tweet_json['user']['id_str'])
                ttwython.send_direct_message(screen_name=id_to_dm, text="Blocked twitter.com/sjwomble/status/"+tweet_json['id_str'])
        elif mute_block_off == "mute":
            if tweet_json['user']['id_str'] not in ids_muted:  
                # Mute built in API call missing for some reason, hence call to post
                ttwython.post("mutes/users/create",params=dict(user_id=tweet_json['user']['id_str']))
                global ids_muted
                ids_muted.append(tweet_json['user']['id_str'])
                # Send the message   
                ttwython.send_direct_message(screen_name=id_to_dm, text="Muted twitter.com/sjwomble/status/"+tweet_json['id_str'])
        

def getFriends(friends):
    end_time = time.time()
    global start_time
    print "Time elapsed =", end_time - start_time
    # If 10 minutes since last check then get followers. Don't want to do each time or it will run out of API calls and slow down block/mute
    if end_time - start_time > 600:
        # Get follower ids... NB ONLY WORKS FOR <5000 followers! TODO: Fix ... 
       friends = [str(id) for id in ttwython.get_friends_ids()['ids']] 
       start_time = time.time()
       print "reset time, friends reloaded"
    
    return friends   
 
if __name__ == '__main__':
    # Get details of the application you created as part of the bot process
    APP_KEY = os.getenv('APP_KEY') 
    APP_SECRET = os.getenv('APP_SECRET')
    OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')
    OAUTH_TOKEN_SECRET = os.getenv('OAUTH_TOKEN_SECRET')
    # Get your Twitter id
    id_to_track = os.getenv('TWITTER_ID')
    # get the id to send DMs to
    id_to_dm = os.getenv('TWITTER_ID_DM')
    # Set environment entry for mute/block/off - controls if the personal bot is muting, blocking or off. 
    os.environ["MUTE_BLOCK_OFF"] = "mute"
	
    print "Initialising personal block bot for: ",id_to_track
        
    # twitter object for sending DMs / muting / blocking
    ttwython = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    # Get user id
    twitter_num_id = ttwython.lookup_user(screen_name=id_to_track)[0]['id_str']
    
    # Arrays for people blocked and muted. TODO: Store to DB and recover from there. 
    # Will also not pick up manual blocks and mutes as only runs at startup
    ids_blocked = [str(id) for id in ttwython.list_block_ids()['ids']]
    #No mute API call! Have to do manually ... 
    ids_muted = [str(id) for id in ttwython.get("mutes/users/ids")['ids']]
    # Get friends
    my_friends = [str(id) for id in ttwython.get_friends_ids()['ids']]                                                      

    # Start the streamer...
    stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=id_to_track)
