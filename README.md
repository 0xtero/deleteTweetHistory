deleteTweetHistory
==================

This small script goes through your Twitter timeline and deletes your old @reply tweets from it.
You can configure a date threshold and e-mail address. The deleted tweets will be e-mailed to you for archiving.

Note! 
No warranty. If you manage to delete your entire timeline, only YOU are to blame. Use at your own risk.

License: Totally completely Public Domain. Do whatever you want with it.

Why?
----
Because you might not want your old conversations around for years and years. Of course they'll probably be cached in various other places, but
at least this way the link to your account will be broken. It's not perfect privacy (or really, privacy at all) - but then again nothing on Twitter is. 

Pre-reqs and Installation.
--------------------------

You'll need 
* Python 3.x
* Twython (https://github.com/ryanmcgrath/twython/)
* Access to SMTP-server running at localhost if you want the e-mail

In order to run it, you need to:
* Login to Twitter dev (https://dev.twitter.com/
* Go to "My Apps" (https://dev.twitter.com/apps)
* Create New App and fill in the stuff they want (you don't need callback URL)
* Once done, go to the API keys tab
* Open config.ini and fill in the API key and secret, the app will try to do Oauth to fill in the rest. You'll want to keep your config.ini somewhere safe.


Usage
------

Most of this stuff should be fairly self-explanatory 

<pre>
usage: deleteTweetHistory.py [-h] [-m foo@bar.com] [-d YYYYMMDD] [-t]

Deletes old @reply conversations from Twitter.

optional arguments:
  -h, --help      show this help message and exit
  -m foo@bar.com  send report to this e-mail address.
  -d YYYYMMDD     delete tweets older than this date.
  -t              test run, don't actually delete anything.
  </pre>
  
 The optional -m switch sends the deleted tweets to your mailbox for archiving. 
 Try it out with the -t test-switch first so you don't lose anything valuable
 