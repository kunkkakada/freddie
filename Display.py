from Message import *

import pygame
from pygame.locals import *
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

WALL_HEIGHT = 3.5
CAMERA_HEIGHT = 500.0

VIEW_2D = 0
VIEW_2D_CENTER = 1
VIEW_3D_FPS = 2
 
class Display:
	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
		self.xwidth = 800
		self.ywidth = 600
		self.walls = []
		self.characters = {}
		self.screen = pygame.display.set_mode((self.xwidth, self.ywidth), DOUBLEBUF|OPENGL)

		self.midpoint = [np.round(self.xwidth / 2), np.round(self.ywidth / 2)]
		self.views = [VIEW_2D, VIEW_2D_CENTER, VIEW_3D_FPS]
		self.view = self.views.pop(0)

		self.debugprints = 1
		self.wallfill = 0

		# TODO: load in a function and store in a dictionary
		self.wall_texture_id = self.load_image('img/wall1.png')

		# Enable depth testing to prevent drawn objects overlapping
		glEnable(GL_DEPTH_TEST)

		# Set perspective settings
		glMatrixMode(GL_PROJECTION)
		gluPerspective(60, (self.xwidth / self.ywidth), 0.1, 10000.0)
		glMatrixMode(GL_MODELVIEW)

		# Set perspective to default camera
		self.default_camera()

	def load_image(self, filename):
		im = Image.open(filename)
		# Todo: return/save image sizes as well
		ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGBA", 0, -1)
		texture_id = glGenTextures(1)

		glBindTexture(GL_TEXTURE_2D, texture_id)
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

		return texture_id

	def select_camera(self):
		for key, value in self.characters.iteritems():
			if value[2] != 'player':
				continue
			pos = value[0]
			direction = value[1]
			cdir = np.array([direction[0], direction[1]])

		glLoadIdentity()
		if self.view == VIEW_2D:
			self.default_camera()
		else:
			self.set_camera(pos, cdir)

	def default_camera(self):
		gluLookAt(0, 0, CAMERA_HEIGHT, 0, 0, 0, -1, 0, 0)

	def set_camera(self, pos, cdir):
		if self.view == VIEW_2D_CENTER:
			gluLookAt(pos[0], pos[1], CAMERA_HEIGHT, pos[0], pos[1], 0, cdir[0], cdir[1], 0)
		elif self.view == VIEW_3D_FPS:
			gluLookAt(pos[0], pos[1], pos[2] + 1.5, pos[0] + 1.0 * cdir[0], pos[1] + 1.0 * cdir[1], pos[2] + 1.5, 0, 0, 1.0)

	def draw_player(self, ppos, pdir):
		self.draw_player_2d(ppos, pdir)

	def draw_player_2d(self, ppos, pdir):
		linend = np.add(np.array([ppos[0], ppos[1]]), 10 * pdir)

		# Draw player direction vector
		if self.view <= VIEW_2D_CENTER:
			glBegin(GL_LINES)	
			glColor3d(1, 1, 1)
			glVertex3f(int(np.round(ppos[0])), int(np.round(ppos[1])), int(np.round(ppos[2])))
			glVertex3f(linend[0], linend[1], ppos[2])
			glEnd()

			# Draw dot
			glEnable(GL_POINT_SMOOTH)
			glPointSize(5 + ppos[2] / 10.0)

			glBegin(GL_POINTS)
			glColor3d(1, 0, 0)
			glVertex3d(ppos[0], ppos[1], ppos[2])
			glEnd()

	def draw_npcs(self):
		for key, value in self.characters.iteritems():
			if value[2] == 'player':
				continue

			cpos = character[0]
			direction = character[1]
			cdir = np.array(direction[0], direction[1])

			# TODO Draw character

	def draw_walls(self, ppos, pdir):
		for idx, wall in enumerate(self.walls):		
			if self.view == VIEW_2D or self.view == VIEW_2D_CENTER:
				self.draw_wall_2d(wall)
			
			elif self.view == VIEW_3D_FPS:
				self.draw_wall_3d(wall)

	def draw_wall_2d(self, wall):
		glBegin(GL_LINES)
		glColor3d(0, 1, 0)
		glVertex3f(wall.x1, wall.y1, 0.0)
		glVertex3f(wall.x2, wall.y2, 0.0)
		glEnd()

		# Draw dots
		# LEFT = RED
		glEnable(GL_POINT_SMOOTH)
		glPointSize(5)

		glBegin(GL_POINTS)
		glColor3d(1, 0, 0)
		glVertex3d(wall.x1, wall.y1, 0.0)
		glEnd()

		# RIGHT = BLUE
		glEnable(GL_POINT_SMOOTH)
		glPointSize(5)

		glBegin(GL_POINTS)
		glColor3d(0, 0, 1)
		glVertex3d(wall.x2, wall.y2, 0.0)
		glEnd()

	def draw_wall_3d(self, wall):
		glEnable(GL_TEXTURE_2D)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
		glBindTexture(GL_TEXTURE_2D, self.wall_texture_id)

		wall_length = np.sqrt(np.power(wall.x2 - wall.x1, 2) + np.power(wall.y2 - wall.y1, 2))
		# TODO use im.size
		u = wall_length / (256.0 / 512.0 * 4.5)

		glBegin(GL_QUADS)
		glColor3d(0, 1, 0)

		glTexCoord2f(0.0, 0.0)
		glVertex3f(wall.x1, wall.y1, 0.0)

		glTexCoord2f(0.0, 1.0)
		glVertex3f(wall.x1, wall.y1, WALL_HEIGHT)

		glTexCoord2f(u, 1.0)
		glVertex3f(wall.x2, wall.y2, WALL_HEIGHT)

		glTexCoord2f(u, 0.0)
		glVertex3f(wall.x2, wall.y2, 0.0)

		glEnd()
		glDisable(GL_TEXTURE_2D)

	def update(self):
		# Clear screen
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		self.screen.fill(BLACK)

		# Get player position
		for key, value in self.characters.iteritems():
			# TODO: handle multiple players?
			if value[2] != 'player':
				continue
			ppos = value[0]
			direction = value[1]
			pdir = np.array([direction[0], direction[1]])

		# Draw player
		self.draw_player(ppos, pdir)

		# Draw other characters
		self.draw_npcs()
			
		# Draw walls
		self.draw_walls(ppos, pdir)

		# Draw floor
		glBegin(GL_QUADS)

		glColor3d(0.12, 0.08, 0.08)
		glVertex3f(-200.0, -200.0, 0.0)
		glVertex3f(-200.0, 200.0, 0.0)
		glVertex3f(200.0, 200.0, 0.0)
		glVertex3f(200.0, -200.0, 0.0)

		glEnd()

		# Select camera based on view
		self.select_camera()

				
	def handle_message(self, msg):
		#  Switch camera
		if msg.msg_type==MsgType.INPUT:
			if msg.content['cmd']=='switch camera forward':
				self.views.append(self.view)
				self.view = self.views.pop(0)
				self.update()

			if msg.content['cmd']=='switch camera backward':
				self.views.insert(0,self.view)
				self.view = self.views.pop()
				self.update()

		if msg.msg_type==MsgType.LOAD:
			if msg.content['group'] == 'wall':
				self.walls = msg.content['wall list']
			if msg.content['group'] == 'character':
				self.characters[msg.content['tag']] = [msg.content['pos'], msg.content['towards'], msg.content['type']]
		if msg.msg_type==MsgType.SCENE:
			if msg.content['group'] == 'character':
				self.characters[msg.content['tag']] = [msg.content['pos'], msg.content['towards'], msg.content['type']]
		if msg.msg_type==MsgType.CONSOLE:
			if msg.content['to'] == 'display' or msg.content['to'] == 'all':
				if msg.content['cmd'] == 'debugprints':
					self.debugprints = msg.content['val']
			if msg.content['to'] == 'display':
				if msg.content['cmd'] == 'wallfill':
					self.wallfill = msg.content['val']
		
		return

