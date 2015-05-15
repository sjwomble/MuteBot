#!/bin/bash
# This script sets up Heroku + your local environment for Twitter and the mute bot

# Prerequisite for running -> You need LINUX, (TODO: Create a .bat version for Windows)
# Prerequisite -> Have been through the Heroku tutorial or be experienced with Heroku already (Linux only at the moment) 
# --> https://devcenter.heroku.com/articles/getting-started-with-python#introduction
# NB: If you have completed the tutorial remember to delete the example application before trying to install this one
# You only get ONE free dyn with Heroku. 

echo "Twitter Personal Block Bot"
echo -n "Enter a name - (Suggestion <your_twitter_id>_PBBOT "
read botname

echo -e "\ninitializing git repo"
git init

# Removed " --stack cedar" from the example used, this is deprecated now and presumably not needed, cedar-14 is the current stack. 
while ! heroku create $botname; do
    echo "We failed to create the Heroku app"
    echo -n "Try another name? "
    read botname
done

echo
echo "We're going to need some Twitter API credentials."
echo "Check out https://dev.twitter.com/docs/auth/tokens-devtwittercom"
echo "for instructions on creating your Consumer Key and Access Token."
echo "Be sure to set to Access Level to \"Read and write AND direct messages\" in the Settings tab."
# TODO: Write post
echo "Read the accompanying blog post at sjwomble.wordpress.com/<url> for more information>"
echo

confirmed_creds="n"
while [ $confirmed_creds != "y" ]; do

    echo -n "Consumer key: "
    read consumerkey
    echo -n "Consumer secret: "
    read consumersecret
    echo -n "Access token: "
    read accesstoken
    echo -n "Access token secret: "
    read accesstokensecret
    echo -n "User this is to be installed for (Example: \"sjwomble\", no @: "
    read twitterid
    echo "User to DM tweets that initiated a mute or block to? (Example: \"sjwomble\", no @: "
    echo "This can be your account, or an alt you've set up to monitor potentially abusive tweets, even a friend willing to check them. "
    echo "If you are being dogpiled, you might want to turn off notifications for DMs for yours or the alt account! "
    echo -n "Twitter id for DMs (Example: \"sjwomble\", no @: "
    read twitterid_dm

    echo "We read these credentials:"
    cat <<EOF
APP_KEY=$consumerkey
APP_SECRET=$consumersecret
OAUTH_TOKEN=$accesstoken
OAUTH_TOKEN_SECRET=$accesstokensecret
TWITTER_ID=$twitterid
TWITTER_ID_DM=$twitterid_dm
EOF
    echo "Is this correct? [y/n]"
    read confirmed_creds
done

#add the twitter credentials to the Heroku app environment
echo
echo "Sending your Twitter API credentials and twitter id up to Heroku..."
heroku config:add APP_KEY=$consumerkey \
    APP_SECRET=$consumersecret \
    OAUTH_TOKEN=$accesstoken \
    OAUTH_TOKEN_SECRET=$accesstokensecret \
    TWITTER_ID=$twitterid \
    TWITTER_ID_DM=$twitterid_dm

#create a script for setting up your local environment
cat <<EOF > setup_env.sh
export APP_KEY=$consumerkey
export APP_SECRET=$consumersecret
export OAUTH_TOKEN=$accesstoken
export OAUTH_TOKEN_SECRET=$accesstokensecret
export TWITTER_ID=$twitterid
export TWITTER_ID_DM=$twitterid_dm
EOF


# Push to Heroku and start the Dyno
echo -e "\npushing to heroku\n"
git add .
git commit -m 'added all files'
git push heroku master
heroku ps:scale worker=1

# DB section - add the PostGreSQL DB addon and create any tables required (TODO: Add when DB coded) 
#echo -e "\nAdding PostGreSQL DB addon\n"
#heroku addons:add heroku-postgresql:hobby-dev
#echo -e "\nWaiting for DB to start\n"
#heroku pg:wait

echo -e "done! your bot should now be running on heroku.\n type heroku logs --tail to make sure."

# If you have a verified heroku account (Have added a credit card), install this useful addon. Can be ran after setup.
# Allows tables to be viewed / inspected to see who is blocked/muted
# heroku addons:add pgstudio
