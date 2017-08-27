
class Scene:
	
	def __init__(self):
		self.walls = []
		self.doors = []
		self.objects = [] # Non-pickables
		self.items = [] # Pickables
		self.player = None
		self.characters = []
		
	def load_scene(self, scenefile):
		print "TODO"

	def update(self, timestep):
		print "TODO"
