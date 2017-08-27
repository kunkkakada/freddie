# X is left-right
# Y is forwards-backwards
# Z is up-down

import pygame
import math
import time

def screen_coords(x, y):
	return ((x / 2 + 0.5) * SCREEN_WIDTH, (-y / 2 + 0.5) * SCREEN_HEIGHT)

def rad(degrees):
	return degrees / 180 * math.pi;

# Returns x of intersecting point with x-axis on graph
def intersect(x1, y1, x2, y2):
	return (y1 * x2 - y2 * x1) / (y1 - y2)

def move_player_pos(mult, rot_disp):
	global pos
	x = pos[0] + math.sin(rad(rot + rot_disp)) * SPEED * mult
	y = pos[1] + math.cos(rad(rot + rot_disp)) * SPEED * mult
	pos = (x, y)

WIDTH = 1200
HEIGHT = 400
SCREENS = 3
SCREEN_WIDTH = WIDTH / SCREENS
SCREEN_HEIGHT = HEIGHT

WALLS = [
	((-1.0, 1.0), (1.0, 1.0), (150, 150, 150)),
	((1.0, 1.0), (1.0, -1.0), (255, 150, 255)),
	((1.0, -1.0), (0.5, -1.5), (150, 255, 255)),
	((-0.5, -1.5), (-1.0, -1.0), (255, 255, 150)),
	((-1.0, -1.0), (-1.0, 1.0), (150, 255, 150))]
WALL_HEIGHT = 0.25

SPEED = 0.01
ROT_SPEED = 2
RAY_LENGTH = 0.1

PLAYER_COLOR = (0, 255, 0)
PLAYER_RAY_COLOR = (255, 0, 0)

CEILING_COLOR = (0, 0, 255)
FLOOR_COLOR = (255, 255, 0)

FRAME_MIN = 0.016

pos = (0., 0.)
rot = 0. # 0 is north, clockwise, degrees

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

prev_time = time.time()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Handle keys

	keys = pygame.key.get_pressed()
	
	if keys[pygame.K_LEFT]:
		rot -= ROT_SPEED
	if keys[pygame.K_RIGHT]:
		rot += ROT_SPEED
	
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		move_player_pos(1, 0)
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		move_player_pos(-1, 0)
	if keys[pygame.K_d]:
		move_player_pos(1, 90)
	if keys[pygame.K_a]:
		move_player_pos(-1, 90)
	
	# Set up split screen rendering surface

	split_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

	###########################################################################
	# SCREEN 1: STATIC WORLD

	# Clear split screen

	split_screen.fill((0, 0, 0))

	# Draw wall

	for wall in WALLS:
		# Wall absolute positions
		x1 = wall[0][0]
		y1 = wall[0][1]
		x2 = wall[1][0]
		y2 = wall[1][1]
		
		pygame.draw.line(split_screen, wall[2],
			screen_coords(x1, y1),
			screen_coords(x2, y2), 1)	

	# Draw player

	pygame.draw.line(split_screen, PLAYER_RAY_COLOR,
		screen_coords(pos[0], pos[1]),
		screen_coords(
			pos[0] + math.sin(rad(rot)) * RAY_LENGTH,
			pos[1] + math.cos(rad(rot)) * RAY_LENGTH), 1)
	pygame.draw.line(split_screen, PLAYER_COLOR,
		screen_coords(pos[0], pos[1]),
		screen_coords(pos[0], pos[1]), 1)

	# Render split screen

	screen.blit(split_screen, (0, 0))

	###########################################################################
	# SCREEN 2: STATIC PLAYER

	# Clear split screen

	split_screen.fill((0, 0, 0))

	# Draw wall
	
	for wall in WALLS:
		# Wall absolute positions
		x1 = wall[0][0]
		y1 = wall[0][1]
		x2 = wall[1][0]
		y2 = wall[1][1]

		# Wall positions relative to player's position
		px1 = x1 - pos[0]
		py1 = y1 - pos[1]
		px2 = x2 - pos[0]
		py2 = y2 - pos[1]

		# Wall positions relative to player's position and rotation
		rx1 = math.cos(rad(-rot)) * px1 + math.sin(rad(-rot)) * py1
		ry1 = math.cos(rad(-rot)) * py1 - math.sin(rad(-rot)) * px1
		rx2 = math.cos(rad(-rot)) * px2 + math.sin(rad(-rot)) * py2
		ry2 = math.cos(rad(-rot)) * py2 - math.sin(rad(-rot)) * px2

		pygame.draw.line(split_screen, wall[2],
			screen_coords(rx1, ry1),
			screen_coords(rx2, ry2), 1)

	# Draw player

	pygame.draw.line(split_screen, PLAYER_RAY_COLOR,
		screen_coords(0, 0),
		screen_coords(0, RAY_LENGTH), 1)
	pygame.draw.line(split_screen, PLAYER_COLOR,
		screen_coords(0, 0),
		screen_coords(0, 0), 1)

	# Render split screen

	screen.blit(split_screen, (SCREEN_WIDTH, 0))
	
	###########################################################################
	# SCREEN 3: PERSPECTIVE

	# Clear split screen

	split_screen.fill((0, 0, 0))

	# Draw wall, floor and ceiling
	
	pygame.draw.rect(split_screen, CEILING_COLOR, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
	pygame.draw.rect(split_screen, FLOOR_COLOR, pygame.Rect(0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2))

	for wall in WALLS:
		# Wall absolute positions
		x1 = wall[0][0]
		y1 = wall[0][1]
		x2 = wall[1][0]
		y2 = wall[1][1]

		# Wall positions relative to player's position
		px1 = x1 - pos[0]
		py1 = y1 - pos[1]
		px2 = x2 - pos[0]
		py2 = y2 - pos[1]

		# Wall positions relative to player's position and rotation
		rx1 = math.cos(rad(-rot)) * px1 + math.sin(rad(-rot)) * py1
		ry1 = math.cos(rad(-rot)) * py1 - math.sin(rad(-rot)) * px1
		rx2 = math.cos(rad(-rot)) * px2 + math.sin(rad(-rot)) * py2
		ry2 = math.cos(rad(-rot)) * py2 - math.sin(rad(-rot)) * px2

		# Don't render walls behind us
		if ry1 <= 0 and ry2 <= 0:
			continue

		# Clip walls intersecting with user plane
		if ry1 <= 0 or ry2 <= 0:
			ix1 = intersect(rx1, ry1, rx2, ry2)
			if ry1 <= 0:
				rx1 = ix1
				ry1 = 0.01
			if ry2 <= 0:
				rx2 = ix1
				ry2 = 0.01
		
		# Wall positions relative to player's position, rotation and perspective
		zx1 = rx1 / ry1
		zu1 = WALL_HEIGHT  / ry1 # Up   Z
		zd1 = -WALL_HEIGHT / ry1 # Down Z
		zx2 = rx2 / ry2
		zu2 = WALL_HEIGHT  / ry2 # Up   Z
		zd2 = -WALL_HEIGHT / ry2 # Down Z

		pygame.draw.polygon(split_screen, wall[2], [
			screen_coords(zx1, zd1),
			screen_coords(zx1, zu1),
			screen_coords(zx2, zu2),
			screen_coords(zx2, zd2)], 0)

	# Render split screen

	screen.blit(split_screen, (SCREEN_WIDTH * 2, 0))

	# Render split screen lines

	pygame.draw.line(screen, (255, 255, 255),
		(SCREEN_WIDTH, 0),
		(SCREEN_WIDTH, SCREEN_HEIGHT), 2)
	pygame.draw.line(screen, (255, 255, 255),
		(SCREEN_WIDTH * 2, 0),
		(SCREEN_WIDTH * 2, SCREEN_HEIGHT), 2)

	# Update screen

	pygame.display.update()
	
	# Sleep
	
	new_time = time.time()
	diff_time = new_time - prev_time
	prev_time = new_time
	if diff_time < FRAME_MIN:
		time.sleep(FRAME_MIN - diff_time)
