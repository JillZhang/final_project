import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import socket
import json
import sys
consumer_key = '5O7d4or6khFOr07uDEy4nMcNf'
consumer_secret = 'bAOn4OLWRxgVtcw0RmaBY667bctWj4uaqGFOgHXaTq1OI45cU0'
access_token = '843631973860040712-ulSvFRFkk9JEa2Ujdi2ivoQPKzlZlIz'
access_secret = 'cK5u2FtO5luSs9Kn1pBbzkGi97ARxdbubwbVtwBygexYo'

class TweetsListener(StreamListener):

  def __init__(self, csocket):
      self.client_socket = csocket

  def on_data(self, data):
      try:
          msg = json.loads( data )
          #print( msg['text'].encode('utf-8') )
          self.client_socket.send( str(data).encode('utf-8') )
          return True
      except BaseException as e:
          #print("Error on_data: %s" % str(e))
          return True
      return True

  def on_error(self, status):
      print(status)
      return True

def sendData(c_socket):
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_secret)

  twitter_stream = Stream(auth, TweetsListener(c_socket))
  twitter_stream.filter(track=['a','you','u','and','i','is','are','was'])

if __name__ == "__main__":
  s = socket.socket()         # Create a socket object
  host = "localhost"      # Get local machine name
  port = 4444                 # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print( "Received request from: " + str( addr ) )

  sendData( c )
