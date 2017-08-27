import numpy as np
from Message import *


JUMPSPEED = 5.0
WALKSPEED = 0.5
TURNSPEED = 3.0
G = 9.81

class Player:
	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
		self.pos = np.array([20,20,0], dtype=float) # x, y, z
		self.vel = np.array([0,0,0], dtype=float) # vx, vy ,vz
		self.towards = np.array([1,0,0], dtype=float) # 
		self.turnleft = 0
		self.turnright = 0
		self.moveforward = 0
		self.movebackward = 0
		self.sector = None
		self.load_jump = None
	
	def handle_message(self, msg):
		if msg.msg_type==MsgType.INPUT:
			if msg.content['cmd']=='jump':
				self.load_jump=msg.content['time']
			elif msg.content['cmd']=='stop jump':
				self.vel[2]+=min(1000, msg.content['time']-self.load_jump)*JUMPSPEED
				self.load_jump = None
			elif msg.content['cmd']=='forward':
				self.moveforward = 1
				#self.vel += (proj_normalize(self.towards)*WALKSPEED) 
			elif msg.content['cmd']=='backward':
				self.movebackward = 1
			elif msg.content['cmd']=='stop forward':
				self.vel = np.array([0,0,self.vel[2]])
				self.moveforward = 0
			elif msg.content['cmd']=='stop backward':
				self.vel = np.array([0,0,self.vel[2]])
				self.movebackward = 0
			elif msg.content['cmd']=='turn left':
				self.turnleft = 1
			elif msg.content['cmd']=='turn right':
				self.turnright = 1
			elif msg.content['cmd']=='stop turn right':
				self.turnright = 0
			elif msg.content['cmd']=='stop turn left':
				self.turnleft = 0
		return
		
		
	def update(self, dt):
		self.pos += dt*self.vel
		
		self.pos[2] = max(0, self.pos[2])
		if self.pos[2]:
			self.vel[2]-=G*dt
		else:
			self.vel[2]=0
		if self.turnleft!=0:
			self.towards = rotate(self.towards, TURNSPEED)
		if self.turnright!=0:
			self.towards = rotate(self.towards, -TURNSPEED)
			
		if self.moveforward!=0 and self.movebackward!=0:	
			self.vel = np.array([0,0,self.vel[2]])
		elif self.moveforward!=0:
			self.vel = (proj_normalize(self.towards)*WALKSPEED)
		elif self.movebackward!=0:
			self.vel = -(proj_normalize(self.towards)*WALKSPEED) 
			
		if np.linalg.norm(self.vel)>0 or self.turnleft!=0 or self.turnright!=0:
			self.print_player()
		return
	
	def print_player(self):
		print "Player information"
		print "     position: ", self.pos
		print "     velocity: ", self.vel
		print "     orientation: ", self.towards



def normalize(vector):
	return vector/np.linalg.norm(vector)
	
def proj_normalize(vector):
	tmp = np.array([vector[0], vector[1], 0])
	return normalize(tmp)
	
	
def rotate(vector, angle):
	a = np.deg2rad(angle)
	R = np.zeros((3,3), dtype=float)
	R[0,0] = np.cos(a)
	R[0,1] = np.sin(a)
	R[1,0] = -R[0,1]
	R[1,1] = R[0,0]
	return np.dot(R, vector)
	
	
		
