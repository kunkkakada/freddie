from Objects import *

class Scene:
	
	def __init__(self):
		self.walls = []
		self.doors = []
		self.non_pickables = []
		self.pickables = [] 
		self.player = None
		self.characters = []
		self.mesh = None
		
	def load_scene(self, objectfile):
		# 1. load mesh
		# 2. load objects
		# 2.1 create ids for objects
		tag = 1
		f = open(objectfile, 'r')
		wall_line = f.readline().split()
		n_walls = int(wall_line[1])
		for i in range(n_walls):
			wall_line = f.readline().split()
			x1 = float(wall_line[0])
			x2 = float(wall_line[1])
			y1 = float(wall_line[2])
			y2 = float(wall_line[3])
			h = float(wall_line[4])
			col = (int(wall_line[5]), int(wall_line[6]), int(wall_line[7]))
			self.walls.append(Wall(tag, x1, x2, y1, y2, h, col))
			tag +=1
		
		
		

	def update(self, timestep):
		print "TODO"

	def handle_message(self, msg):
		return
