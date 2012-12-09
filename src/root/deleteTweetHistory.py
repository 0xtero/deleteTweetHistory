#!/usr/bin/python

# Deletes Twitter @reply history, sends the deleted tweets in e-mail for private archiving

import argparse
import datetime
import tweepy
from tweepy import Cursor
import ConfigParser

def doLogin(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)    
    return tweepy.API(auth)

def findTweets(session, vDate):
    api = session
    lTempTweets = []
    # Get tweets - Twitter API only returns max 800 replies.
    tweets = Cursor(api.user_timeline, count=3200, include_rts=True)
    for tweet in tweets.items():
        if tweet.text.startswith("@"):
            # it"s a reply
            if vDate >= tweet.created_at:
                # it"s old enough
                lTempTweets.append(tweet)
    return lTempTweets

def doDelete(session, lDestroy): 
    api = session
    for tweet in lDestroy:
        api.destroy_status(tweet.id)
    return

def doReport(lTweetList):
    vToday = datetime.datetime.today()
    vTempReport = "This report was generated: {}\n".format(vToday)
    vTempReport += "Following tweets were deleted\n"
    for tweet in lTweetList:
        vTempReport += "\t{}\t{}\t{}\n".format(tweet.id, tweet.created_at, tweet.text.encode('utf-8'))
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
    parser.add_argument("-d", metavar="YYYYMMDD", type=str, help="delete tweets older than this date.")
    parser.add_argument("-t", action="store_true", help="test run, don't actually delete anything.")
    args = parser.parse_args()

    vTargetDate = datetime.datetime.strptime(args.d,"%Y%m%d")
    vEmail = args.m
    vTest = args.t
    lDeleteTweets = []
    
    # Read config.ini for OAUTH strings
    config = ConfigParser.RawConfigParser()
    config.read("config.ini")
    CONSUMER_KEY = config.get("OAUTH", "CONSUMER_KEY")
    CONSUMER_SECRET = config.get("OAUTH", "CONSUMER_SECRET")
    ACCESS_TOKEN = config.get("OAUTH", "ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = config.get("OAUTH", "ACCESS_TOKEN_SECRET")
    
    # Authenticate session
    session = doLogin(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    # Return tweet ID*s for deleteable tweets
    lDeleteTweets = findTweets(session, vTargetDate)
    # Don't delete if -t is defined
    if not vTest:
        doDelete(session,lDeleteTweets)
    # Build the report body
    vReport = doReport(lDeleteTweets)
    print vReport
    # And e-mail it
    sendEmail(vEmail,vReport)
    