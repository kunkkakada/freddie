import pygame
import numpy as np
from pygame.locals import *
from Message import *

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

ix1 = 600
ix2 = 600
iy1 = 200
iy2 = 400
northvector = [0,-1]
WALL_HEIGHT = 0.5
	
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between180(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    
def angle_between360(v1,v2):
	dot = np.dot(v1,v2)      # dot product
	det = v1[0]*v2[1] - v1[1]*v2[0]      # determinant
	return np.arctan2(det, dot)

def rotate(vec, angle):
	rotmatrix = np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
	val = np.dot(rotmatrix,[vec[0],vec[1]])
	return val
	
def rotate_eye(vec, angle):
	val = [vec[0]*np.cos(angle)-vec[1]*np.sin(angle), vec[0]*np.sin(angle)+vec[1]*np.cos(angle)]
	return [val[0], -val[1]] 	
	
# Returns x of intersecting point with x-axis on graph
def intersect(x1, y1, x2, y2):
	return (y1 * x2 - y2 * x1) / (y1 - y2)
        
class Display:

	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
		self.xwidth = 800
		self.ywidth = 600
		self.walls = []
		self.characters = {}
		self.screen = pygame.display.set_mode((self.xwidth, self.ywidth))
		self.midpoint = [np.round(self.xwidth/2), np.round(self.ywidth/2)]
		self.views = [0,1,2]
		self.view = self.views.pop(0)
		self.debugprints = 1
		self.wallfill = 0

	def transform(self, ppos, pdir, point):
		xr = point[0]-ppos[0]
		yr = point[1]-ppos[1]
		ang = angle_between360(pdir,northvector)
		#print np.rad2deg(ang)
		w = rotate([xr,yr],ang)
		return w+self.midpoint
		
	def transform_eye(self, ppos, pdir, point):
		xr = point[0]-ppos[0]
		yr = point[1]-ppos[1]
		ang = angle_between360(pdir,northvector)
		#print np.rad2deg(ang)
		w = rotate_eye([xr,yr],ang)
		return w
		
	def update(self):
		for posTowards in self.characters.values():
			#print posTowards[0]
			#print posTowards[1]
			ppos = np.array(posTowards[0])
			direction = posTowards[1]
			pdir = np.array([direction[0], direction[1]])
			# draw on the surface object
		self.screen.fill(BLACK)

		if self.view == 0:
			linend = np.add(np.array([ppos[0],ppos[1]]),20*pdir)
			pygame.draw.circle(self.screen, RED, (int(np.round(ppos[0])),int(np.round(ppos[1]))), 1)
			pygame.draw.line(self.screen, BLUE, (int(np.round(ppos[0])),int(np.round(ppos[1]))), (linend[0], linend[1]))

		if self.view == 1:
			pygame.draw.circle(self.screen, RED, (np.round(self.xwidth/2),np.round(self.ywidth/2)), 2)
			pygame.draw.line(self.screen, BLUE, (np.round(self.xwidth/2)-1,np.round(self.ywidth/2)),(np.round(self.xwidth/2)-1,np.round(self.ywidth/2)-20))
			
		for wall in self.walls:
			ix1 = int(wall.x1)
			ix2 = int(wall.x2)
			iy1 = int(wall.y1)
			iy2 = int(wall.y2)
			
			[wx1, wy1] = self.transform(ppos, pdir, [ix1,iy1,0])
			[wx2, wy2] = self.transform(ppos, pdir, [ix2,iy2,0])
		
		
			if self.view == 0:
				pygame.draw.circle(self.screen, RED, (ix1,iy1), 2)
				pygame.draw.circle(self.screen, BLUE, (ix2,iy2), 2)
				pygame.draw.line(self.screen, GREEN, (ix1,iy1), (ix2,iy2))
			
			if self.view == 1:
				pygame.draw.circle(self.screen, RED, (np.round(self.xwidth/2),np.round(self.ywidth/2)), 2)
				pygame.draw.line(self.screen, BLUE, (np.round(self.xwidth/2)-1,np.round(self.ywidth/2)),(np.round(self.xwidth/2)-1,np.round(self.ywidth/2)-20))
				pygame.draw.circle(self.screen, RED, (int(wx1),int(wy1)), 2)
				pygame.draw.circle(self.screen, BLUE, (int(wx2),int(wy2)), 2)
				pygame.draw.line(self.screen, GREEN, (wx1,wy1), (wx2,wy2))
			
			if self.view == 2:
				w1 = self.transform_eye(ppos, pdir, [ix1,iy1,0])
				w2 = self.transform_eye(ppos, pdir, [ix2,iy2,0])
				
				if w1[1] <= 0 and w2[1] <= 0:
					continue
					
				# Clip walls intersecting with user plane
				if w1[1] <= 0 or w2[1] <= 0:
					ix1 = intersect(w1[0], w1[1], w2[0], w2[1])
					if w1[1] <= 0:
						w1[0] = ix1
						w1[1] = 0.01
					if w2[1] <= 0:
						w2[0] = ix1
						w2[1] = 0.01
				
				# Wall positions relative to player's position, rotation and perspective
				zx1 = self.xwidth*w1[0] / w1[1] + self.midpoint[0]
				zu1 = self.ywidth*WALL_HEIGHT  / w1[1] +self.midpoint[1] # Up   Z
				zd1 = self.ywidth*-WALL_HEIGHT / w1[1] +self.midpoint[1] # Down Z
				zx2 = self.xwidth*w2[0] / w2[1] + self.midpoint[0]
				zu2 = self.ywidth*WALL_HEIGHT  / w2[1] +self.midpoint[1] # Up   Z
				zd2 = self.ywidth*-WALL_HEIGHT / w2[1] +self.midpoint[1]# Down Z

				if self.debugprints == 1:
					print w1[0], w1[1], w2[0], w2[1]
					print zx1, zu1, zd1, zx2, zu2, zd2

				pygame.draw.polygon(self.screen, GREEN, [
					(zx1, zd1),
					(zx1, zu1),
					(zx2, zu2),
					(zx2, zd2)], self.wallfill)

				
	def handle_message(self, msg):
		#  Switch camera
		if msg.msg_type==MsgType.INPUT:
			if msg.content['cmd']=='switch camera forward':
				self.views.append(self.view)
				self.view = self.views.pop(0)
			if msg.content['cmd']=='switch camera backward':
				self.views.insert(0,self.view)
				self.view = self.views.pop()
		if msg.msg_type==MsgType.LOAD:
			if msg.content['group'] == 'wall':
				self.walls = msg.content['wall list']
			if msg.content['group'] == 'character':
				self.characters[msg.content['tag']] = [msg.content['pos'],msg.content['towards']]
		if msg.msg_type==MsgType.SCENE:
			if msg.content['group'] == 'character':
				self.characters[msg.content['tag']] = (msg.content['pos'],msg.content['towards'])
		if msg.msg_type==MsgType.CONSOLE:
			if msg.content['to'] == 'display' or msg.content['to'] == 'all':
				if msg.content['cmd'] == 'debugprints':
					self.debugprints = msg.content['val']
			if msg.content['to'] == 'display':
				if msg.content['cmd'] == 'wallfill':
					self.wallfill = msg.content['val']
		
		return

