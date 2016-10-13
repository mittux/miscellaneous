"""
    This script captures English language tweets from Twitter's Public
    stream and then uses coroutines to broadcast it to different functions
    The downstream functions find tweets with a given pattern and also the
    total number of tweets with those patterns
"""
import sys
import datetime as dt
from twitter import *
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup

tweetCount = 0
TWEETCOUNT = 1000

try:
    from mytwitter import *
except ImportError:
    print("*** Keys and Access Tokens not set! ***")

auth_details = OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)


def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next(cr)
        return cr
    return start


def tweetor():
    global tweetCount
    global tweet_generator

    while tweetCount < TWEETCOUNT:

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
                return tweet
        else:
            pass

    return 'Done'


def data_pipe(iterator, target):
    while True:
        twt = iterator()
        if twt:
            target.send(twt)
        if twt == 'Done':
            return


@coroutine
def printer():
    global tweetCount
    while True:
        tweet = (yield)
        print ('[%s] [%s] tweeted: %s' % (tweetCount, tweet['user']['screen_name'], tweet['text']))


@coroutine
def grep(pattern, target):
    count = 0
    while True:
        twt = (yield)  # Receive a tweet
        if twt == 'Done': # print the number of tweets with the pattern
            print('\n*** %d tweets with \'%s\' ***'% (count, pattern))
        else:
            if pattern in twt['text'].lower():
                target.send(twt)  # Send to next stage
                count += 1

# Broadcast a stream onto multiple targets
@coroutine
def broadcast(targets):
    while True:
        item = (yield)
        for target in targets: # sequential dispatch
            target.send(item)


def main():
    twitter_stream = TwitterStream(auth=auth_details)

    print("*** Sampling Twitter Public stream *** ")
    global tweet_generator
    tweet_generator = twitter_stream.statuses.sample()

    startTime = dt.datetime.now()

    data_pipe(tweetor, broadcast([grep('trump',  printer()),
                                  grep('brexit', printer())]))

    stopTime = dt.datetime.now()

    print('\n*** %d tweets captured from %s to %s ***'% (TWEETCOUNT, startTime, stopTime))

if __name__ == '__main__':
    sys.exit(main())
