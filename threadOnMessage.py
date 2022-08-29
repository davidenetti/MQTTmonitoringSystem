#!/usr/bin/env python3

import threading
from threading import Thread
import time
import mysql.connector
import re
import sys
import paho.mqtt as mqtt

# Set up a connection to the postgres DB.
def connectToDB():
    print("I'm connecting to DB...\n")
    connectionValue = mysql.connector.connect (
        host = "localhost",
        user = "root",
        passwd = "DavideMacbook1996"
    )
    return connectionValue

# Check if a host that i see, has already been seen
def checkHostInDB(hostMacAddress):
    print("I'm check if the host is already in DB or not...\n")
    connectionFromDB = connectToDB()
    mycursor = connectionFromDB.cursor()
    QUERY = "SELECT COUNT(*) FROM `networkMonitoring`.`hostSeen` WHERE `MacAddress` = %s;"
    mycursor.execute(QUERY, (str(hostMacAddress),))
    returnedValue = mycursor.fetchone()
    numOfElements = int(returnedValue[0])
    
    if(numOfElements == 1):
        print("OK, host is already in DB!")
        return True
    else:
        print("Host isn't in DB!")
        return False

# Add host to the table which keeps track of whether it has seen a particular host.
def addHostToDB(hostMacAddress):
    print("I'm adding the host to DB")
    connectionFromDB = connectToDB()
    mycursor = connectionFromDB.cursor()
    QUERY =  "INSERT INTO `networkMonitoring`.`hostSeen`(`MacAddress`) VALUES (%s);"
    mycursor.execute(QUERY, (str(hostMacAddress),))
    macAddressReturned= mycursor.lastrowid
    if(macAddressReturned != None):
        print(str(macAddressReturned) + "\n")
        connectionFromDB.commit()

# This function takes care of loading into the database, the data that is periodically sent to me by the hosts.
def loadDataToDB(connectionParameters, hostname, IPAddress, MacAddress, startTime):

    receivingTime = time.time()


    #Calculate the difference between two time interval (propagation)
    startTimeInMilliseconds = int(round(float(startTime) * 1000))
    receivingTimeInMilliseconds = int(round(time.time() * 1000)) #TimeStampStored

    differenceBetweenTimesInMilliseconds = receivingTimeInMilliseconds - startTimeInMilliseconds

    #All 3 times converted to more beatiful format and to string
    receivingTimeToString = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(receivingTime)) 
    startTimeToString = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(startTime)) 
    propagation = str(differenceBetweenTimesInMilliseconds)


    print("I'm loading data...\n")
    connectionFromDB = connectToDB()
    mycursor = connectionFromDB.cursor()
    
    QUERY = "INSERT INTO `networkMonitoring`.`hostInformation`(`IPaddress`, `HostName`, `TimeStampReceived`, `TimeStampStored`, `Propagation`, `MacAddress`) VALUES (%s, %s, %s, %s, %s, %s);"

    mycursor.execute(QUERY, (str(IPAddress), str(hostname), startTimeToString, receivingTimeToString, propagation, str(MacAddress)))

    print("Insert done!\n")
    connectionFromDB.commit()

#Lock declaration
threadLock = threading.Lock()

class ThreadOnMessage(Thread):
    def __init__(self, MessageIN):
        Thread.__init__(self)
        self.MessageIN = MessageIN

    def run(self):
        # Extract the variables
        MessageIN = self.MessageIN

        hostname = MessageIN["hostname"]
        IPAddress = MessageIN["IPAddress"]
        MacAddress = MessageIN["MacAddress"]
        startTime = MessageIN["StartTime"] #This is equal to TimeStampReceived        
        
        threadLock.acquire()
        #If I have never met the host then add it to DB
        if(checkHostInDB(MacAddress) == False):
            addHostToDB(MacAddress)

        #In each case do...
        connectionParameters = connectToDB()
        loadDataToDB(connectionParameters, hostname, IPAddress, MacAddress, float(startTime))
        threadLock.release()