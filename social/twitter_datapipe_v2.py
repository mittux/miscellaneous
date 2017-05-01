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


def tweetor():
    global tweetCount
    global tweet_generator

    while tweetCount < TWEETCOUNT:

        #for tweet in tweet_generator:
            tweet = next(tweet_generator)
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
                    yield (tweetCount, tweet)
            else:
                pass

    raise StopIteration

def data_pipe(target):
    yield from target

def printer():
    while True:
         count, tweet = (yield)
         print('[%s] [%s] tweeted: %s' % (count, tweet['user']['screen_name'], tweet['text']))

def main():

    twitter_stream = TwitterStream(auth=auth_details)

    print("*** Sampling Twitter Public stream *** ")
    global tweet_generator
    tweet_generator = twitter_stream.statuses.sample()

    startTime = dt.datetime.now()

    pr = printer()
    dpipe = data_pipe(pr)
    dpipe.send(None) # prime

    for tweet in tweetor():
        dpipe.send(tweet)

    stopTime = dt.datetime.now()

    print('\n*** %d tweets captured from %s to %s ***'% (TWEETCOUNT, startTime, stopTime))

if __name__ == '__main__':
    sys.exit(main())
