#!/usr/bin/env python3

import threading
from threading import Thread
import paho.mqtt.client as mqtt
import sys
import threadOnMessage
import re
import json
import threadOnMessageFromPubAfterCheck

#Broker connection parameters
broker_url = "test.mosquitto.org"
broker_port = 1883

#Global variables
threadsOperatesOnMessage = []

#Action to execute when arrive a new message from publisher
def on_connect(client, userdata, flags, rc):
    if(rc == 0):
        print("Connected succesfully")
    else:
        print("Bad connection, returned code: " + str(rc))

def on_message(client, userdata, message):
    global threadsOperatesOnMessage

    if(re.match("^networkInformationAbout\/([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\/from$", message.topic) != None):
        #Translate the JSON message to a python object
        messageIN=json.loads(message.payload.decode())

        #Call a thread that operates
        threadsOperatesOnMessage.append(threadOnMessage.ThreadOnMessage(messageIN))
        lastThread = len(threadsOperatesOnMessage) - 1
        
        #Start and join threads
        threadsOperatesOnMessage[lastThread].start()
        threadsOperatesOnMessage[lastThread].join()

    if(re.match("^checkFromWebServer\/([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\/to$", message.topic) != None):
        #Call a thread that operates
        threadOperatesOnMessage = threadOnMessageFromPubAfterCheck.ThreadOnMessageFromPubAfterCheck(message.payload.decode())
        
        #Start and join threads
        threadOperatesOnMessage.start()
        threadOperatesOnMessage.join()

client = mqtt.Client("subscriberClient", True)
client.connect(broker_url, broker_port)
client.on_connect = on_connect
client.on_message = on_message
client.subscribe([("checkFromWebServer/+/to", 1), ("networkInformationAbout/+/from", 1)])


try:
    client.loop_forever()
except(KeyboardInterrupt, SystemExit):
    raise