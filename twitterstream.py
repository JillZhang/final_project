#! /usr/bin/python

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import signal
import sys
import json

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after

consumer_key="5O7d4or6khFOr07uDEy4nMcNf"
consumer_secret="bAOn4OLWRxgVtcw0RmaBY667bctWj4uaqGFOgHXaTq1OI45cU0"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="843631973860040712-ulSvFRFkk9JEa2Ujdi2ivoQPKzlZlIz"
access_token_secret="cK5u2FtO5luSs9Kn1pBbzkGi97ARxdbubwbVtwBygexYo"

class StdOutListener(StreamListener):

    def __init__(self, path):
        self.path = path + "/tweets-"
        self.file_count = 0
        self.f = open(self.path + str(self.file_count) + ".json", 'a')

        signal.signal(signal.SIGINT, self.signal_handler)

    def on_data(self, data):
        if (self.f.tell() > 1048576):
            self.close_open()
        self.write_to_file(data)
        return True

    def on_error(self, status):
        print(status)

    def close_open(self):
        self.f.close()
        self.file_count += 1
        self.f = open(self.path + str(self.file_count) + ".json", 'a')

    def write_to_file(self, data):
        # data is a json object
        json.dump(data, self.f)
        self.f.write('\n')

    def signal_handler(self, signal, frame):
        print('You pressed Ctrl+C!')
        self.f.close()
        sys.exit(0)



if __name__ == '__main__':
    if (len(sys.argv) < 2): 
        print("needs a path argument")
        sys.exit(0)
    else :
        path = sys.argv[1]
        l = StdOutListener(path)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = Stream(auth, l)
        stream.filter(track=['protest', 'demonstration', 'rally', 'riot', 'march'])

