"""
    This script captures English language tweets from Twitter's Public
    stream and then stores them in to a MongoDB database
"""
import sys
import datetime as dt
from twitter import *
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter_db import *

TWEETCOUNT = 1000

try:
	from mytwitter import *
except ImportError:
	print("*** Keys and Access Tokens not set! ***")

class databaseEntry(object):
    def __init__(self, user, userid, userdescription, created, location, timezone, tweet, tweetid, hashtags):
        self.user = user
        self.userid = userid
        self.userdescription = userdescription
        self.created = created
        self.location = location
        self.timezone = timezone
        self.tweet = tweet
        self.tweetid = tweetid
        self.hashtags = hashtags

    def encodeData(self):
        # stripping down JSON to simple "variable-sized" dictionary for MongoDB
        data = {}
        # These fields are expected
        data['user'] = self.user
        data['userid'] = self.userid
        data['tweet'] = self.tweet
        data['tweetid'] = self.tweetid
        data['created'] = self.created
        # These fields are not guaranteed
        if self.location is not None:
            data['location'] = self.location
        if self.timezone is not None:
            data['timezone'] = self.timezone
        if self.location is not None:
            data['userdescription'] = self.userdescription
        if bool(self.hashtags):
            data['hashtags'] = self.hashtags
        return data

def main():
    # TODO: any way to re-attempt if stream is not established, and then give up gracefully?
    twitter_stream = TwitterStream(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET))

    db = TwitterDataBase()

    # delete tweets from last run
    db.removeAllTweets()

    tweetCount = 0
    startTime = dt.datetime.now()

    while tweetCount < TWEETCOUNT:

        iterator = twitter_stream.statuses.sample()
        print("*** Sampling Twitter Public stream *** ")
    
        for tweet in iterator:
            if tweet is None:
                    print("-- None --")
            elif tweet is Timeout:
                print("-- Timeout --")
            elif tweet is HeartbeatTimeout:
                print("-- Heartbeat Timeout --")
            elif tweet is Hangup:
                print("-- Hangup --")
            elif tweet.get('text'):
                if tweet.get('lang') == 'en':
                    print('[{}] [{}] tweeted: {}'.format(tweetCount+1, tweet['user']['screen_name'], tweet['text']))
                    db.insertTweet(databaseEntry(tweet['user']['screen_name'],
                                                 tweet['user']['id_str'],
                                                 tweet['user']['description'],
                                                 tweet['created_at'],
                                                 tweet['user']['location'],
                                                 tweet['user']['time_zone'],
                                                 tweet['text'],
                                                 tweet['id_str'],
                                                 tweet['entities']['hashtags']).encodeData())
                    tweetCount += 1
                    if tweetCount >= TWEETCOUNT:
                        break
            else:
                pass

    stopTime = dt.datetime.now()

    print('\n*** %d tweets captured from %s to %s ***'% (TWEETCOUNT, startTime, stopTime))


if __name__ == '__main__':
    sys.exit(main())