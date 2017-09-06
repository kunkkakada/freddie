


class Wall:
	
	def __init__(self, x1, x2, y1, y2, height, col):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.height = height
		self.col = col


		#self.doors = []
	
	#def add_door(door):
		#self.doors.append(door)



class Door:
	
	def __init__(self, x1, x2, y1, y2, height, col, locked):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.height = height
		self.col = col
		self.opened = False
		self.locked = locked
		
	def operate():
		if self.opened:
			self.opened=False
		else:
			self.opened = True
			
	def unlock():
		if self.locked:
			self.locked=False
		
