#!/usr/bin/env python3

import threading
from threading import Thread
import json
import time
import socket
from getmac import get_mac_address as gma

#Lock declaration
threadLock = threading.Lock()


def informationAboutTheHost():
	result = []
	try:
		#IP address
		result.append(str(socket.gethostname()))
		#Hostname
		result.append(socket.gethostbyname(str(result[0])))
		#MacAddress
		result.append(gma())
	except: 
		print("Unable to get Hostname, IP and MacAddress")

	try:
		#Time since epoch in seconds
		result.append(str(time.time()))

	except:
		print("Unable to append time")

	return result

class ThreadPublishAMessage(Thread):
	def __init__(self, client):
		Thread.__init__(self)
		self.client = client

	def run(self):
		# Extract the variables
		client = self.client
		
		result = informationAboutTheHost()

		dictonaryMessageOut = {
			"hostname": str(result[0]),
			"IPAddress": str(result[1]),
			"MacAddress": str(result[2]),
			"StartTime": str(result[3])
		}
		

		JSONMessageOut = json.dumps(dictonaryMessageOut)

		threadLock.acquire()
		#Publishing the hostname, IP address, MacAddress and "start time"
		print("I'm publishing a messagge...")
		client.publish(topic="networkInformationAbout/" + str(result[2]) + "/from", payload = JSONMessageOut, qos=1, retain=True)
		threadLock.release()
		print("Message published!")