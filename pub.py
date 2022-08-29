#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import re
import time
import threadPublishAMessage
from getmac import get_mac_address as gma
import threadMessageReceivedFromInterface

#Action to execute when arrive a new message from publisher
def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print("Connected succesfully")
    else:
        print("Bad connection, returned code: " + str(rc))

def on_message(client, userdata, message):
	threadOnMessage = threadMessageReceivedFromInterface.ThreadMessageReceivedFromInterface(message, client)

	#Execute and join code in thread
	threadOnMessage.start()
	threadOnMessage.join()

broker_url = "test.mosquitto.org"
broker_port = 1883

client = mqtt.Client(str(gma()), True)
client.connect(broker_url, broker_port)
client.on_connect = on_connect
client.on_message = on_message
client.subscribe([("checkFromWebServer/all", 1), ("checkFromWebServer/" + str(gma()), 1)])

try:
	client.loop_start()
except (KeyboardInterrupt, SystemExit):
	raise

while True:
	time.sleep(40)
	#Call a thread to build a message and publish it
	threadPublishPeriodicMessage = threadPublishAMessage.ThreadPublishAMessage(client)

	#Execute and join code in thread
	threadPublishPeriodicMessage.start()
	threadPublishPeriodicMessage.join()