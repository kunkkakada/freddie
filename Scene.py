from Objects import *
from Player import *


class Scene:
	
	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
		self.walls = []
		self.doors = []
		self.non_pickables = []
		self.pickables = [] 
		self.player = Player()
		self.characters = []
		self.mesh = None

		
		msg = Message(MsgType.SCENE)
		msg.content = {'tag': id(self.player), 'group': 'character', 'pos': self.player.pos, 'towards': self.player.towards}
		self.msg_bus.post_message(msg)
		
	def load_scene(self, objectfile):
		# 1. load mesh
		# 2. load objects
		
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
			self.walls.append(Wall(x1, x2, y1, y2, h, col))
		msg = Message(MsgType.SCENE)
		msg.content = {'group': 'wall', 'wall list': self.walls}
		self.msg_bus.post_message(msg)
		

	def update(self, timestep):
		self.player.update(timestep)

	def handle_message(self, msg):
		self.player.handle_message(msg)
		return

	
