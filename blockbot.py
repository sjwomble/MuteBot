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

# Streaming class for Twython, infinite loop so all the work needs to be done from here!
class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            # Print tweet to logs
            print data['text'].encode('ascii','ignore') 
            # Need to check is the tweet from the person being tracked and @'ing themselves, so a command? 
            if data['text'].startswith("@"+id_to_track) & data['user']['screen_name'].startswith(id_to_track):
                # is a connand message
                handleCommand(data['text'].encode('ascii','ignore'))
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
    print "Potential tweet to handle",tweet_json['text'].encode('ascii','ignore')
    # Only get friends list every 10 mins or it will seriously slow down blocking any dogpiles etc...
    the_friends = getFriends()
    #If friend then do nothing, otherwise block or mute (Or nothing if bot is off
    if tweet_json['user']['id_str'] not in the_friends:  
        mute_block_off = os.getenv('MUTE_BLOCK_OFF')
        msg = ""
        if mute_block_off == "block":
            if tweet_json['user']['id_str'] not in ids_blocked:  
                try:
                    ttwython.create_block(user_id=tweet_json['user']['id_str'])
                except TwythonError as e:
                    print e
                    # retry ... usually works second time!
                    ttwython.create_block(user_id=tweet_json['user']['id_str'])
                # Not ideal as it will only track from start. TODO: put ids blocked by bot into a DB table
                ids_blocked.append(tweet_json['user']['id_str'])
                print "Pushed ",tweet_json['user']['id_str']," into blocks, num in list =",len(ids_blocked)
                ttwython.send_direct_message(screen_name=id_to_dm, text="Blocked twitter.com/sjwomble/status/"+tweet_json['id_str'])
        elif mute_block_off == "mute":
            if tweet_json['user']['id_str'] not in ids_muted:  
                # Mute built in API call missing for some reason, hence call to post
                try:
                    ttwython.post("mutes/users/create",params=dict(user_id=tweet_json['user']['id_str']))
                except TwythonError as e:
                    print e
                    # retry ... usually works second time!
                    ttwython.post("mutes/users/create",params=dict(user_id=tweet_json['user']['id_str']))
                ids_muted.append(tweet_json['user']['id_str'])
                print "Pushed ",tweet_json['user']['id_str']," into mutes, num in list =",len(ids_muted)
                # Send the message   
                ttwython.send_direct_message(screen_name=id_to_dm, text="Muted twitter.com/sjwomble/status/"+tweet_json['id_str'])
        else:
            print "Personal block bot off, no action taken"
    else:
        print "Tweet from friend, no action taken"
        

def getFriends():
    end_time = time.time()
    global start_time
    global my_friends
    print "Time elapsed =", end_time - start_time
    # If 10 minutes since last check then get followers. Don't want to do each time or it will run out of API calls and slow down block/mute
    if end_time - start_time > 600 or len(my_friends) == 0:
        # Get follower ids... NB ONLY WORKS FOR <150000 friends ... You are not following that many people, right? 
        # Obviously slower the more people you are following, especially more blocks of 5K 
        next_cursor=-1
        my_friends =[]
        while(next_cursor):
            following = twitter.get_friends_ids(cursor = next_cursor)
            for id in following['ids']:    
                my_friends.append(str(id))
            next_cursor = following['next_cursor']
        start_time = time.time()
        print "reset timer, friends - ",len(my_friends)," reloaded"
    
    return my_friends   
 
if __name__ == '__main__':
    # Start timer
    global start_time 
    global ids_blocked 
    global ids_muted
    global my_friends
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
    start_time = time.time()
    # twitter object for sending DMs / muting / blocking
    ttwython = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    # Get user id
    twitter_num_id = ttwython.lookup_user(screen_name=id_to_track)[0]['id_str']
    
    # Arrays for people blocked and muted. TODO: Store to DB and recover from there. 
    # Will also not pick up manual blocks and mutes as only runs at startup
    next_cursor=-1
    while(next_cursor):
        ids_blocked = twitter.list_block_ids(cursor = next_cursor)
        for id in ids_blocked['ids']:    
            ids_blocked.append(str(id))
            next_cursor = ids_blocked['next_cursor']
    
    print "Found ",len(ids_blocked)," blocks, added to list"
    
    #No mute API call! Have to do manually ... Works up to 5K mutes, not sure how to pass next_curse - TODO: fix
    ids_muted = [str(id) for id in ttwython.get("mutes/users/ids")['ids']]

    print "Found ",len(ids_muted)," mutes, added to list"
    # Get friends
    my_friends = []
    getFriends()
    
    # Start the streamer...
    stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=id_to_track)
