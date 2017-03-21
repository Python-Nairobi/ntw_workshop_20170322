import time
from umqtt.simple import MQTTClient

# ============================================================================
# environment container
# ============================================================================
env = {
    "MQTT_USER": "",
    "MQTT_PASSWORD": "",
    "MQTT_PORT": "",
    "TW_STREAM_TOPIC": "",
}


# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))


def main(server=env['MQTT_SERVER'],
         user=env['MQTT_USER'],
         password=env['MQTT_PASSWORD'],
         port=env['MQTT_PORT']):

    c = MQTTClient("umqtt_client",
                   server,
                   user=user,
                   password=password,
                   port=port)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(bytes(env['TW_STREAM_TOPIC']))
    while True:
        if True:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()


if __name__ == "__main__":
    main()
