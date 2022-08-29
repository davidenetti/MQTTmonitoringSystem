#!/usr/bin/env python3

import threading
from threading import Thread
import threadPublishAMessage

#Lock declaration
threadLock = threading.Lock()

class ThreadMessageReceivedFromInterface(Thread):
    def __init__(self, messageReceived, client):
        Thread.__init__(self)
        self.messageReceived = messageReceived
        self.client = client

    def run(self):
        # Extract the variables
        messageReceived = self.messageReceived
        client = self.client

        requestedValues = threadPublishAMessage.informationAboutTheHost()
        if(messageReceived.topic == "checkFromWebServer/all" or messageReceived.topic == ("checkFromWebServer/" + str(requestedValues[2]))):
            print("One message received!\n")
            messagePayload = messageReceived.payload.decode()
            if(messagePayload == "Check"):
                threadLock.acquire()

                strPayload = ("My IP: " + str(requestedValues[0]) + " my hostname: " + str(requestedValues[1]) + " and my mac address: " + str(requestedValues[2]) + "\n")

                client.publish(topic="checkFromWebServer/" + str(requestedValues[2]) + "/to", payload = strPayload, qos=1, retain=True)
                threadLock.release()