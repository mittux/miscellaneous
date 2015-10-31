"""
    This script does some analysis of tweets captured from 
    Twitter's Public Stream. It:
    - Finds Most Common Words    
    - Finds Most Common Hashtags
"""
import sys
import re
import collections
import string
from nltk.corpus import stopwords
from twitter_db import *
from pprint import *

def findMostCommonWords(top_n):

    db = TwitterDataBase()

    emoticons_str = r"""
        (?:
         [:=;] # Eyes
         [oO\-]? # Nose (optional)
         [D\)\]\(\]/\\OpP] # Mouth
        )"""
 
    url_str = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs

    regex_str = [
        emoticons_str,
        url_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:[\.]+)', # dots like ...
        r'(?:\S)' # anything else
    ]
    
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    url_re = re.compile(url_str,re.VERBOSE | re.IGNORECASE)

    def preprocess(s, lowercase=False):
        tokens = tokens_re.findall(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    word_counter = collections.Counter();

    # ignore stopwords, punctuations, 'rt', etc.
    ignored = stopwords.words('english') + list(string.punctuation) + ['rt', 'via']

    for t in db.getAllTweets(**{}):
        #print('[{}] tweeted: {}'.format(t['user'], t['tweet']))
        tokenized = [term for term in preprocess(t['tweet'], lowercase=True) if (term not in ignored and not url_re.search(term))]

        for each in tokenized:
            word_counter[each] += 1

    print('Top {} words :'.format(top_n))        
    print(word_counter.most_common(top_n))
    print()


def findMostPopularHashtags(top_n):
    # hastags are already available in the text of the tweet but here
    # it is extracted from mongodb using 'hashtags' key exists query

    hashtags_counter = collections.Counter()

    for t in TwitterDataBase().getAllTweets(**{'hashtags':{ '$exists': 'true'}}):
        for h in t['hashtags']:
            hashtags_counter[h['text']] += 1

    print('Top {} hashtags :'.format(top_n))
    print(hashtags_counter.most_common(top_n))
    print()


def main():
    findMostCommonWords(100)
    findMostPopularHashtags(50)


if __name__ == '__main__':
    sys.exit(main())