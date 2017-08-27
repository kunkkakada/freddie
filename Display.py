import pygame
import numpy as np
from pygame.locals import *

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

class Display:
	
	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
		self.xwidth = 800
		self.ywidth = 600
		self.screen = pygame.display.set_mode((self.xwidth, self.ywidth))

	def update(self, ppos, pdir):
		pdir = np.array([pdir[0], pdir[1]])
		linend = np.add(np.array([ppos[0],ppos[1]]),10*pdir)
		# draw on the surface object
		self.screen.fill(BLACK)
		pygame.draw.circle(self.screen, RED, (int(np.round(ppos[0])),int(np.round(ppos[1]))), 1)
		pygame.draw.line(self.screen, BLUE, (int(np.round(ppos[0])),int(np.round(ppos[1]))), (linend[0], linend[1]))

	def handle_message(self, msg):
		return

