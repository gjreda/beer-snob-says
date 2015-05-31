from collections import defaultdict, deque
from itertools import chain
from twython import Twython
import random
import re
import sys

import config

twitter = Twython(
    config.TWITTER_CONSUMER_KEY,
    config.TWITTER_CONSUMER_SECRET,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_SECRET
)

class MarkovChain(object):
    def __init__(self, documents, **kwargs):
        self.chain_length = kwargs['num'] if 'num' in kwargs.keys() else 3
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
        if len(self.words) < self.chain_length:
            return

        for i in range(len(self.words) - self.chain_length):
            yield_chain = [self.words[i+j] for j in range(self.chain_length)]
            yield (tuple(yield_chain[:-1]),yield_chain[-1])

    def wordbase(self):
        for w,wlast in self.yield_trigrams():
            self.word_cache[w].append(wlast)

    def generate_tweet(self, min_chars=100, max_chars=140):
        seed = random.randint(0, len(self.words) - self.chain_length)
        w = deque([self.words[seed+j] for j in range(self.chain_length - 1)])
        tweet = '  '

        # loop until it's a sentence
        while tweet[-2] not in '.!?':
            w.append(random.choice(self.word_cache[tuple(w)]))            
            tweet += (w.popleft() + ' ')

        # if it's too short or too long, try again
        if len(tweet) < min_chars or len(tweet) > max_chars:
            # If default arguments are changed they need to be sent again
            # down the pipe            
            tweet = self.generate_tweet(min_chars, max_chars)
        return tweet.strip()

def main():
    with open(sys.argv[1]) as f:
        text = [line for line in f]
    tweet = MarkovChain(text, num = 5).generate_tweet()
#    print tweet
    twitter.update_status(status=tweet)

    

if __name__ == '__main__':
    main()
