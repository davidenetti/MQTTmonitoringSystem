import threading
from threading import Thread

#Lock declaration
threadLock = threading.Lock()

class ThreadOnMessageFromPubAfterCheck(Thread):
    def __init__(self, messagePayload):
        Thread.__init__(self)
        self.messagePayload = messagePayload

    def run(self):
        # Extract the variables
        messagePayload = self.messagePayload

        threadLock.acquire()
        print(messagePayload)
        threadLock.release()