deteleTweetHistory
==================

This small script goes through your Twitter timeline and deletes your old @reply tweets from it.
You can configure a date threshold and e-mail address. The deleted tweets will be e-mailed to you for archiving.

Note! 
No warranty. If you manage to delete your entire timeline, only YOU are to blame. Use at your own risk.

License: Totally completely Public Domain. Do whatever you want with it.

Why?
----
Because you might not want your old conversations around for years and years. Of course they'll probably be cached in various other places (like Google), but
at least this way the link to your account will be broken. It's not perfect privacy (or really, privacy at all) - but then again nothing on Twitter is. 

Pre-reqs and Installation.
--------------------------

You'll need 
	* Python 2.x
	* Tweepy (http://tweepy.github.com/)
	* Access to SMTP-server running at localhost

In order to run it, you need to:
	* Login to Twitter dev (https://dev.twitter.com/
	* Go to "My Apps" (https://dev.twitter.com/apps)
	* Create New App
	* Once done, go to the OAuth tab
	* Open config.ini and fill in the required OAuth strings

That's it - it's pretty basic OAuth Twitter app setup.

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
  
 The -m switch sends the deleted tweets to your mailbox for archiving. 
 Try it out with the -t test-switch first so you don't lose anything valuable
 
 Limitations
 ------------
 * Clients may not make more than 350 requests per hour, so if you have a lot of tweets to delete, you'll hit this. There's no error handling, sorry. The script will just probably terminate.
 * It returns total of 3200 tweets (and then iterates through those to check for old replies). I have no idea what happens if you have more.

 Author
 ------
 Tero Hänninen <tero@hanninen.eu>