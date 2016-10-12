"""
    This script captures English language tweets from Twitter's Public
    stream and then using coroutines sends it down a data pipe which prints it
    on the screen
"""
import sys
import datetime as dt
from twitter import *
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup

tweetCount = 0
TWEETCOUNT = 100

try:
    from mytwitter import *
except ImportError:
    print("*** Keys and Access Tokens not set! ***")

auth_details = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start

@coroutine
def printer():
    global tweetCount
    while True:
         tweet = (yield)
         print '[%s] [%s] tweeted: %s' % (tweetCount+1, tweet['user']['screen_name'], tweet['text'])

def tweetor():
    global tweetCount
    global tweet_generator

    while tweetCount < TWEETCOUNT:

        for tweet in tweet_generator:
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
                    if tweetCount >= TWEETCOUNT:
                        break
                    tweetCount += 1
                    return tweet
            else:
                pass

    return 'Complete'


def data_pipe(iterator, target):
    while True:
        twt = iterator()
        if twt == 'Complete':
            return
        if twt:
            target.send(twt)

def main():

    twitter_stream = TwitterStream(auth=auth_details)

    print("*** Sampling Twitter Public stream *** ")
    global tweet_generator
    tweet_generator = twitter_stream.statuses.sample()

    startTime = dt.datetime.now()

    data_pipe(tweetor, printer())

    stopTime = dt.datetime.now()

    print('\n*** %d tweets captured from %s to %s ***'% (TWEETCOUNT, startTime, stopTime))

if __name__ == '__main__':
    sys.exit(main())