
class MsgType:
    
    NONE = 1
    INPUT = 2
    SCENE = 3
    SCREEN = 4
    SOUND = 5
    EVENT = 6
    LOAD = 7

class Message:
    def __init__(self, msg_type):
        self.msg_type = msg_type
        self.content = None # Dictionary with keys 'obj', 'action', 'param'
	
class MessageBus:
	def __init__(self):
		self.systems = {} # Dictionary of systems with MsgType as key
		self.msg_list = []

	def post_message(self, msg):
		self.msg_list.append(msg)
	
	def print_message_bus(self):
		if len(self.msg_list)>0:
			print "printing message bus:"
		for i, msg in enumerate(self.msg_list):
			print i+1, msg.msg_type, msg.content
		#print "done"
