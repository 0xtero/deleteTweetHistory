#!/usr/bin/python

# Deletes Twitter @reply history, sends the deleted tweets in e-mail for private archiving

import argparse
import datetime
from twython import Twython
from twython import TwythonError
from twython import TwythonRateLimitError
import configparser


def doTwitterAuth(api_key, api_secret):
	az = Twython(api_key, api_secret)
	auth = az.get_authentication_tokens()
	print("Get PIN from: " + auth['auth_url'])
	auth_pin = input('Enter the PIN: ')
	final_tokens = az.get_authorized_tokens(auth_pin.rstrip('\n'))
	oauth_token = final_tokens['oauth_token']
	oauth_secret = final_tokens['oauth_token_secret']
	# Write the tokens to config for future use
	config = configparser.ConfigParser()
	oauth = config['OAUTH']
	oauth['API_KEY'] = api_key
	oauth['API_SECRET'] = api_secret
	oauth['OAUTH_TOKEN'] = oauth_token
	oauth['OAUTH_SECRET'] = oauth_secret
	with open('config.ini', 'w') as configfile:
		config.write(configfile)
	return(oauth_token, oauth_secret)

def findTweets(twitter, vDate):
	lTempTweets = []
	max_loops = 10
	max_tweets = 2000
	next_max_id = None 
	
	# Page through max_loops x 200 tweets
	for i in range(0,max_loops):
		# Return if we get over max_tweets
		if(max_tweets < len(lTempTweets)):
			return (lTempTweets)
		
		# First time around get the 200 latest tweets
		if(0 == i):
			results = twitter.get_user_timeline(include_rts='false', count='200')
		# after that get the next 200 from max_id
		else:
			results = twitter.get_user_timeline(include_rts='false', count='200', max_id=next_max_id)
		
		# loop through results        
		for tweet in results:
			# it's a reply
			next_max_id = tweet['id_str']
			if (tweet['in_reply_to_user_id'] != None):
				tweet_date = datetime.datetime.strptime(tweet['created_at'],"%a %b %d %H:%M:%S %z %Y")
				simple_date = datetime.datetime.date(tweet_date)
				# it's older than specified date
				if (vDate >= simple_date):
					# save it
					lTempTweets.append(tweet)
					
	return (lTempTweets)

def doDelete(twitter, lDestroy): 
	lTempDelTweets = []
	# loop through tweets...
	for tweet in lDestroy:
		# check if the api allows for more tries..
		try:
			# Finally, try to delete something
			try:
				# but don't if -t flag is on..
				if not vTest:
					twitter.destroy_status(id = tweet['id'])
					# save it..
					lTempDelTweets.append(tweet)
					# Catch exception and exit the loop	
			except TwythonError as e:
				print (e)
				break
		except TwythonRateLimitError:	
			print ("No available Twitter API requests. Try again in 15 minutes. Exiting.\n")
			break
	return(lTempDelTweets)

def doReport(lTweetList):
    vToday = datetime.datetime.today()
    vTempReport = "This report was generated: {}\n".format(vToday)
    vTempReport += "Following tweets were deleted\n"
    for tweet in lTweetList:
        vTempReport += "\t{}\t{}\t{}\n".format(tweet['id_str'], tweet['created_at'], tweet['text'])
    return(vTempReport)
    
def sendEmail(vEmailAddress, vMessageBody):    
    
    import smtplib
    from email.mime.text import MIMEText
    
    vMe = "deleteTweetHistory Report <noreply@foo.bar>"
    vYou = vEmailAddress
    vToday = datetime.datetime.today()
    
    msg = MIMEText(vMessageBody)
    msg["Subject"] = "deleteTweetHistory Report {}".format(vToday)
    msg["From"] = vMe
    msg["To"] = vYou

    s = smtplib.SMTP("localhost")
    s.sendmail(vMe, [vYou], msg.as_string())
    s.quit()
    return
    
if __name__ == "__main__":
    
    # Command line args
    parser = argparse.ArgumentParser(description="Deletes old @reply conversations from Twitter.")
    parser.add_argument("-m", metavar="foo@bar.com", type=str, help="send report to this e-mail address.")
    parser.add_argument("date", metavar="YYYYMMDD", type=str, help="delete tweets older than this date.")
    parser.add_argument("-t", action="store_true", help="test run, don't actually delete anything.")
    args = parser.parse_args()

    vTempDate = datetime.datetime.strptime(args.date,"%Y%m%d")
    vTargetDate = datetime.datetime.date(vTempDate)
    vEmail = args.m
    vTest = args.t
    lDeleteTweets = []
    
    # Read config.ini for OAUTH strings
    config = configparser.ConfigParser()
    config.read("config.ini")
    API_KEY = config.get("OAUTH", "API_KEY")
    API_SECRET = config.get("OAUTH", "API_SECRET")
    if not (config['OAUTH']['OAUTH_TOKEN'] or config['OAUTH']['OAUTH_SECRET']):
    	OAUTH_TOKEN, OAUTH_SECRET = doTwitterAuth(API_KEY, API_SECRET)
    else:
    	OAUTH_TOKEN = config.get("OAUTH", "OAUTH_TOKEN")
    	OAUTH_SECRET = config.get("OAUTH", "OAUTH_SECRET")
    
    twitter = Twython(API_KEY, API_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
    status = twitter.verify_credentials()
    
    # Return deletable tweets
    lDeleteTweets = findTweets(twitter, vTargetDate)
    # Return deleted tweets
    lNukedTweets = doDelete(twitter,lDeleteTweets)
    # Build the report body
    vReport = doReport(lNukedTweets)
    print (vReport)
    # And e-mail it
    if vEmail:
    	sendEmail(vEmail,vReport)
    