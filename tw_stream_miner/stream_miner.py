#!/usr/bin/env python
from os import environ as env
import logging
import paho.mqtt.client as paho
from twitter import OAuth, TwitterStream

#Log file definition
logging.basicConfig(filename=env['LOG_FILE'],level=logging.DEBUG)

# CloudMQTT config items
def on_publish(client, userdata, mid):
    logging.info("mid: "+str(mid))


client = paho.Client()
client.on_publish = on_publish
client.connect('localhost', 8833)


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
        logging.debug(tweet['text'])
        msg_info = client.publish(env['TW_STREAM_TOPIC'], tweet['text'])

        if not msg_info.is_published():
            logging.error('Message is not yet published.')
