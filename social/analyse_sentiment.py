"""
    This script does sentiment analysis of tweets
"""
import sys
import re
import subprocess
from twitter_db import *
import json

def getSentiment(text):
    """
        sentiment comes as JSON after making an HTTP POST to
        http://text-processing.com/api/sentiment/

        This is done using 'curl' command
    """
    curl = subprocess.Popen(["curl", "-d", "text="+text, "http://text-processing.com/api/sentiment/"],
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE)

    for c in curl.stdout:
        return c.decode('utf-8')

def main():
    
    if len(sys.argv) < 2:
        numberToAnalyze = 0
    else:
        numberToAnalyze = int(sys.argv[1])

    emoticons_str = r"""
        (?:
         [:=;] # Eyes
         [oO\-]? # Optional Nose 
         [D\)\]\(\]/\\OpP] # Mouth
        )"""
 
    url_str = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs

    ignore_str = [
                   emoticons_str,
                   url_str,
                   r'\#',
                   r'\@',
                   r'[\s]*RT[\s]+'
    ]

    ignore_re = re.compile(r'('+'|'.join(ignore_str)+')', re.VERBOSE|re.IGNORECASE)

    db = TwitterDataBase()

    for t in db.getNTweets(numberToAnalyze):

        # clean up tweet before evaluating sentiment
        filtered_tweet = ignore_re.sub('',t['tweet'])

        # if the tweet already has a sentiment, don't bother
        if 'sentiment' not in t.keys():
            sentiment = getSentiment(filtered_tweet)
            db.addNewKey(mongo_id=t['_id'], key='sentiment', **json.loads(sentiment))


if __name__ == '__main__':
    sys(exit(main()))

