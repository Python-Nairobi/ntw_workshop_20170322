#!/usr/bin/env python
from os import environ as env
import paho.mqtt.client as paho
from twitter import OAuth, TwitterStream


# CloudMQTT config items
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))


client = paho.Client()
client.on_publish = on_publish
client.connect('localhost', 1833)


# Twitter app config items
stream = TwitterStream(
    auth=OAuth(
        env['TW_ACCESS_TOKEN'],
        env['TW_ACCESS_SECRET'],
        env['TW_CONSUMER_KEY'],
        env['TW_CONSUMER_SECRET']
    )
)
tweets = stream.statuses.filter(track=env['HASH_TAGS'])

for tweet in tweets:
    if 'RT' not in tweet['text']:
        print tweet['text']
        msg_info = client.publish('jojo_snls/dj_jojo_test', tweet['text'])

        if not msg_info.is_published():
                print('Message is not yet published.')
