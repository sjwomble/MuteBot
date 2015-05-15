# PersonalBlockBot
Bot for Twitter, install and control who can send you mentions. 

GO TO post -> https://sjwomble.wordpress.com/2015/05/15/your-personalblockbot/

INSTALL INSTRUCTIONS

If you do not have a Linux machine you can use (Possibly OSX, not tested) and you are not at all technical then you will struggle, this has not been tested deploying on Windows but it is likely not too hard. If stuck, complete step one below and ask a friend (Or me thesjwomble@gmail.com) to set this up for you, you will need to give the person you ask the keys to the application you create and your Heroku login. So make sure you trust them.

Step One. Create a Twitter application; (You will need a phone number associated with your Twitter account)

    Go to apps.twitter.com, select "Create New App" at the top right of the page. Fill out the values, like this.
    Go to the permissions section and make sure direct messages are allowed, like this. Click on "Update Settings".
    Go to Keys and Access tokens, select the Generate Access Token and Secret at the bottom of the page. You should then have a page that looks like this. Check the permissions includes DMs, revisit (2) if not...
    Keep a note of the keys somewhere safe, or leave the browser window open. You'll need them in the next section, or to give to the person setting the bot up for you.

Step Two. Set up your local environment**

    Have a read of the "Getting Started" section in Heroku, https://devcenter.heroku.com/articles/getting-started-with-python#introduction
    Follow the setup for creating a Heroku account
    Install Python, optional, no need to install Virtualenv unless you want to try the whole tutorial
    In part two, "Set up", there are instructions for installing Heroku Toolbelt. Afterwards, login to Heroku on the command line.

** This is primarily for Linux, however Windows has support for Heroku. You'll just need to extract the commands from the setup.sh ran in the next section and manually issue them.

Step Three. Download, configure and deploy the application on Heroku

    Install git, if you don't have it already!
    Find a directory to place the code, run >git clone https://github.com/sjwomble/PersonalBlockBot
    Go into the directory, cd PersonalBlockBot and run >./setup.sh **
    Enter the values for name, Twitter app keys (Step One above), account name to track and send DMs to. Then the code will push all the settings and code to Heroku and start the bot!
    Try >heroku logs --tail in the directory once you've deployed it. You should see something like this. Any errors contact me.

** If you are translating this to Windows, you need to create the app, set up the environment variables then push to Heroku. That's it!
