NONETYPE = 0
INPUT = 1
GRAPHIC = 2
SOUND = 3
EVENT = 4



class Message:
	def __init__(self, type, content):
		self.type = type
		self.content = content
	
		
