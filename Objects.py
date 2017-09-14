


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
		

class Weapon:
	def __init__(self, name, damage, mag_size, reload_rate, fire_rate, cat):
		self.name = name
		self.damage = damage
		self.mag_size = mag_size
		self.reload_rate = reload_rate
		self.fire_rate = fire_rate
		self.mag = 0
		self.cat = cat # 0,1,2,3,4,5 with 0 fist, 1 'crossbow', 2 'pistol', 3 'shotgun', 4 'rifle', 5 'rocketlauncher'
		
		
	def rload(bullets):
		reloaded_bullets = 0
		if bullets>0:
			reloaded_bullets = min(bullets, mag_size-mag) 
			mag += reloaded_bullets
			bullets -= reloaded_bullets
		return reloaded_bullets
			
			
			
	def shoot():
		if mag:
			mag -= 1
			return self.damage
		return 0
			
		
		
		
		
		
		
		
		
		
	

	
