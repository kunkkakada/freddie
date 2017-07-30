
class MsgType:
    
    NONE = 1
    INPUT = 2
    SCENE = 3
    SCREEN = 4
    SOUND = 5
    EVENT = 6

class Message:
    def __init__(self, msgType):
        self.type = msgType
        self.content = None # Dictionary with keys 'obj', 'action', 'param'
	
class MessageBus:
    def __init__(self):
        self.systems = {} # Dictionary of systems with MsgType as key
        self.msgList = []

    def addSystem(self, key, value):
        self.systems[key] = value
                
    def postMessage(self, msg):
        self.msgList.append(msg)

    def cleanMessageBus(self):
        # Send messages out from the messagebus to correct receivers
        while len(self.msgList)>0:
            # Select correct system depending on the message type, handle message and remove from bus
            msg = self.msgList.pop(0)
            system = self.systems[msg.type]
            system.handleMessage(msg)

