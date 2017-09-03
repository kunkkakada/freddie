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
        
class Display:

	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
		self.xwidth = 800
		self.ywidth = 600
		self.screen = pygame.display.set_mode((self.xwidth, self.ywidth))
		self.midpoint = [np.round(self.xwidth/2), np.round(self.ywidth/2)]
		self.normalview_flag = 0
		self.pers_flag = 1

	def transform(self, ppos, pdir, point):
		xr = point[0]-ppos[0]
		yr = point[1]-ppos[1]
		ang = angle_between360(pdir,northvector)
		print np.rad2deg(ang)
		w = rotate([xr,yr],ang)
		return w+self.midpoint

	def update(self, ppos, pdir):
		pdir = np.array([pdir[0], pdir[1]])
		# draw on the surface object
		self.screen.fill(BLACK)
		[wx1, wy1] = self.transform(ppos, pdir, [ix1,iy1,0])
		[wx2, wy2] = self.transform(ppos, pdir, [ix2,iy2,0])
		
		if self.normalview_flag == 1:
			linend = np.add(np.array([ppos[0],ppos[1]]),20*pdir)
			pygame.draw.circle(self.screen, RED, (int(np.round(ppos[0])),int(np.round(ppos[1]))), 1)
			pygame.draw.line(self.screen, BLUE, (int(np.round(ppos[0])),int(np.round(ppos[1]))), (linend[0], linend[1]))
			pygame.draw.circle(self.screen, RED, (ix1,iy1), 2)
			pygame.draw.circle(self.screen, BLUE, (ix2,iy2), 2)
			pygame.draw.line(self.screen, GREEN, (ix1,iy1), (ix2,iy2))
		
		if self.pers_flag == 1:
			pygame.draw.circle(self.screen, RED, (np.round(self.xwidth/2),np.round(self.ywidth/2)), 2)
			pygame.draw.line(self.screen, BLUE, (np.round(self.xwidth/2)-1,np.round(self.ywidth/2)),(np.round(self.xwidth/2)-1,np.round(self.ywidth/2)-20))
			pygame.draw.circle(self.screen, RED, (int(wx1),int(wy1)), 2)
			pygame.draw.circle(self.screen, BLUE, (int(wx2),int(wy2)), 2)
			pygame.draw.line(self.screen, GREEN, (wx1,wy1), (wx2,wy2))

	def handle_message(self, msg):
		#  Switch camera
		if msg.msg_type==MsgType.INPUT:
			if msg.content['cmd']=='switch camera forward':
				self.normalview_flag ^= 1
				self.pers_flag ^= 1
		if msg.content['cmd']=='switch camera backward':
				self.normalview_flag ^= 1
				self.pers_flag ^= 1
		return

