#!/usr/bin/python2
"""
    This script captures English language tweets from Twitter's Public
    stream and then uses coroutines to broadcast it to different functions
    The downstream functions find tweets with a given pattern and also the
    total number of tweets with those patterns
"""
import sys
import itertools
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


def tweetor():
    global tweetCount
    twitter_stream = TwitterStream(auth=auth_details)
    tweet_generator = twitter_stream.statuses.sample()

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
                yield tweet
        else:
            pass

    raise StopIteration


def grep(pattern):
    global tweetCount
    count = 0
    result = None
    while True:
        twt = (yield result)  # Receive a tweet and yields processed tweet
        if twt == 'Done': # print the number of tweets with the pattern
            result = '\n*** %d tweets with \'%s\' ***'% (count, pattern)
        else:
            if pattern in twt['text'].lower():
                result = '[%s] [%s] tweeted: %s' % (tweetCount, twt['user']['screen_name'], twt['text'])
                count += 1
            else:
                result = None

def done():
    yield 'Done'

def broadcast(source, targets):
    for t in targets:
        next(t)
    for i in itertools.chain(source(), done()):
        result = []
        for t in targets:
            res = t.send(i)
            if res:
                result.append(res)
        if result:
            yield result

def main():

    print("*** Sampling Twitter Public stream *** ")

    startTime = dt.datetime.now()

    for result in broadcast(tweetor, [grep('trump'), grep('brexit')]):
        for r in result:
            print(r)

    stopTime = dt.datetime.now()

    print('\n*** %d tweets captured from %s to %s ***'% (TWEETCOUNT, startTime, stopTime))

if __name__ == '__main__':
    sys.exit(main())
