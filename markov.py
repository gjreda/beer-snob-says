#!/usr/local/bin/python
from collections import defaultdict
from itertools import chain
from twython import Twython
import random
import re
import sys
import time

import config

twitter = Twython(
    config.TWITTER_CONSUMER_KEY,
    config.TWITTER_CONSUMER_SECRET,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_SECRET
)

class MarkovChain(object):
    def __init__(self, documents, **kwargs):
        self.word_cache = defaultdict(list)
        self.words = self.documents_to_words(documents)
        self.word_size = len(self.words)
        self.wordbase = self.wordbase()
    
    def documents_to_words(self, documents):
        """Returns a list of words used in a given list of documents."""
        words = []
        for document in documents:
            if document:
                words.append(self.tokenize(document))
        return list(chain.from_iterable(words))
    
    def tokenize(self, document):
        # don't want empty spaces
        words = [w.strip() for w in document.split() if w.strip() != '']
        return words

    def yield_trigrams(self):
        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 3):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def wordbase(self):
        for w1, w2, w3 in self.yield_trigrams():
            self.word_cache[(w1, w2)].append(w3)

    def generate_tweet(self, min_chars=100, max_chars=140):
        seed = random.randint(0, len(self.words) - 3)
        w1, w2 = self.words[seed], self.words[seed + 1]
        tweet = '  '

        # loop until it's a sentence
        while tweet[-2] not in '.!?':
            if len(w1) > 6 and (random.randint(0,10) > 7):
                tweet += ("#" + w1 + " ")
            else:
                tweet += (w1 + ' ')

            w1, w2 = w2, random.choice(self.word_cache[(w1, w2)])

        # if it's too short or too long, try again
        if len(tweet) < min_chars or len(tweet) > max_chars:
            tweet = self.generate_tweet()
        return tweet.strip()

def main():
    with open(sys.argv[1]) as f:
        text = [line for line in f]
    tweet = MarkovChain(text).generate_tweet().capitalize()
    # wait a random amount of time. A few minutes
    delay = random.randint(0,1200)
    time.sleep(delay)
    # print tweet
    twitter.update_status(status=tweet)

if __name__ == '__main__':
    main()
