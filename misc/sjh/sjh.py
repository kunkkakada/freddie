import pygame, sys
from pygame.locals import *
import math
import random

FPS = 60 # frames per second, the general speed of the program
WINDOWWIDTH = 800 # size of window's width in pixels
WINDOWHEIGHT = 600 # size of windows' height in pixels
C = 0.00065 # wind resistant constant
G=30 # gravity
#imax = 400 # end of the acceleration (global or hill-dependent?)
jump_window = 40 # number of pixels at the end of the slope where the jump is set to take place
telemark_margin = 7.5 # number of pixels (height) to be able to do the telemark 
margin_at_end = 20
dip_when_landing = 20
wind_coeff = 0.001
k_point_coeff = 0.157614243131


thetas = [0, 10, 20, 30, 40, 50, 60, 70, 80]
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)

hills =  ['helsinki', 'monaco', 'casablanca', 'cape town', 'moscow'] #  ['moscow'] #



def main():
	global DISPLAYSURF, font, menufont
	
	
	pygame.init()
	font = pygame.font.Font('etc/INVASION2000.ttf', 25)
	menufont = pygame.font.Font('etc/INVASION2000.ttf', 15)
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Ski Jump Henri 1.0')
	
	while True: # main game loop
		#header = 
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			#elif event.type == KEYDOWN and event.key == pygame.K_DOWN:
		
		
		
		for h in hills:
			player_jump(h)





def player_jump(hill_name):
	global FPSCLOCK, V,A,R,THETA, CameraX, CameraY,imax, MAXWIDTH
	#hill_name = 'cape town' # these parameters from main
	player_name = 'topi'
	
	
	CameraX=0
	CameraY=0
	FPSCLOCK = pygame.time.Clock()


	
	
	k_point, imax, hill_profile, orientation = load_hill(hill_name)
	length_list = calc_len_list(hill_profile,imax)
	k_point_metres = int(length_list[int(k_point)]*k_point_coeff)
	
	MAXWIDTH =  len(orientation)-margin_at_end
	bg = pygame.image.load("etc/bg/{0}.png".format(hill_name))


	
	
	
	V=(0,0)
	A=(0,G)
	R=(0,0)
	shifted=(0,0)
	W=(1.8*(random.random()-0.5),1.8*(random.random()-0.5))
	print W
	points = []
	THETA = 4
	accelerate_image = pygame.image.load('etc/accelerate.png') #TODO image for every position
	wait_image = pygame.image.load('etc/wait.png')
	telemark_image = pygame.image.load('etc/telemark.png')
	tasajalka_image = pygame.image.load('etc/tasajalka.png')
	fall_image = pygame.image.load('etc/fall.png')
	jumper_ims = []
	for t in thetas:
		jumper_ims.append(pygame.image.load('etc/air_{0}.png'.format(t)))
	
	
	
	im = pygame.transform.rotate(wait_image, -math.degrees(math.atan(orientation[int(R[0])])))
	jumper_in_air=False
	jump_started=False
	jump_landed=False
	jump_ready =False
	jump_landing=0 #(0 not yet started, 1 tasajalka, 2 telemark, -1 fall)
	land_text=''
	
	
	draw_hill_from_file(hill_profile,bg,int(k_point), W)
	pygame.display.update()
	
	while jump_ready==False:
		dt = FPSCLOCK.get_time()*1000**-1
		
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN and jump_started==False and col!=RED:
				jump_started=True	           
			elif event.type == KEYDOWN and jump_started==True and jumper_in_air==False and R[0]+jump_window>imax:
				jumper_in_air=True
				V, jumpcoeff = jump(R,V) 
				THETA = 4
				im = jumper_ims[THETA]
				print 'jumping: ',R,V	
			elif event.type == KEYDOWN and jump_landed==True and len(points)==0:
				R = (MAXWIDTH, hill_profile[-margin_at_end])
			elif event.type == KEYDOWN and jump_landed==True and len(points)>0:
				points.sort()
				return jump_len-60.0+points[1]+points[2]+points[3]
			elif event.type == KEYDOWN and jumper_in_air and jump_landing==0:
				if event.key == pygame.K_RIGHT:
					THETA = max(THETA-1, 0)
					im = jumper_ims[THETA]
					print THETA
				if event.key == pygame.K_LEFT:
					THETA = min(THETA+1, len(thetas)-1)
					im = jumper_ims[THETA]
					print THETA
				if event.key == pygame.K_t:
					jump_landing = telemark(R,hill_profile,THETA)
					V = (V[0]*0.5, V[1]+dip_when_landing)
				if event.key == pygame.K_r:
					jump_landing = 1
					V = (V[0]*0.5, V[1]+dip_when_landing)
		
		#### AUTOMATIC JUMP - this is used for testing		
		#if R[0]>imax-0.5*jump_window and jump_started==True and jumper_in_air==False:
			#jumper_in_air=True
			#V, jumpcoeff = jump(R,V) 
			#THETA = 4
			#im = jumper_ims[THETA]
			#print 'jumping: ',R,V
				

		#im = jumper_image kaikkiin
		if jump_landed:
			R,V = deaccelerate(R,V,hill_profile,dt)
			im = pygame.transform.rotate(land_image, -math.degrees(math.atan(orientation[int(R[0])])))
		elif jumper_in_air:
			R,V,A = update_jumper(R,V,A,dt,thetas[THETA],W)			
		elif jump_started:
			R,V = accelerate(R,V,A,hill_profile, dt)
			im = pygame.transform.rotate(accelerate_image, -math.degrees(math.atan(orientation[int(R[0])])))
				

		
		# here checks about the jumber position
		if R[0]>imax and jumper_in_air==False:
			V = (V[0]*0.8, 0)
			jumper_in_air=True
			jumpcoeff = 0
			THETA = 4
			im = jumper_ims[THETA]
			print 'coasting: ', R, V 	    
		
		if R[1]>hill_profile[int(R[0])] and jump_landed==False:
			jump_landed=True
			jump_len = k_point_coeff*length_list[int(R[0])]
			jumper_in_air==False
			if jump_landing==0:
				jump_landing=-1
			if jump_landing==2:
				land_image=telemark_image
				land_text = 'Telemark!'
			elif jump_landing==1:
				land_image=tasajalka_image
				land_text = 'Both feet together...'
			else:
				land_image=fall_image	
				land_text = 'Oh dear, try not to land on your nose!'
			print 'landing: ', R, V
			print 'style: ', jump_landing
		
		# todo calculate points and score and return it here	
		if R[0]>=MAXWIDTH and len(points)==0:
			for i in range(5):
				points.append(referee_points(jumpcoeff,jump_landing))
			#print points
			
		# move the camera
		if R[0]>WINDOWWIDTH/2+CameraX:
			shift_temp = int(R[0]-WINDOWWIDTH/2-CameraX)
			CameraX = min(CameraX+shift_temp, MAXWIDTH-WINDOWWIDTH+margin_at_end)
			
		if R[1]>WINDOWHEIGHT/2+CameraY:
			shift_temp = int(R[1]-WINDOWHEIGHT/2-CameraY)
			CameraY = min(CameraY+shift_temp, max(hill_profile[-1]-WINDOWHEIGHT,0))


			

		
		
		
		#draw_hill(x,y,h,a_2,bg) # this can be commented in testing phase
		draw_hill_from_file(hill_profile,bg,int(k_point),W)
		DISPLAYSURF.blit(im, (R[0]-CameraX,R[1]-15-CameraY))		
		if len(points)>0:
			
			text = font.render(land_text.upper(),1,BLACK)
			len_text = font.render("JUMP LENGTH {0} METRES".format("%.1f" % jump_len),1,BLACK)
			#point_text = font.render("points: {0} {1} {2} {3} {4}".format(points[0],points[1],points[2],points[3],points[4]),1,BLUE)
			point_text = font.render("STYLE POINTS: {0}".format(points),1,BLACK)
			DISPLAYSURF.blit(text, (40, WINDOWHEIGHT-110))
			DISPLAYSURF.blit(len_text, (40, WINDOWHEIGHT-80))
			DISPLAYSURF.blit(point_text, (40, WINDOWHEIGHT-50))
			
		if jump_started==False:
			text = font.render("{0} - {1} METRES".format(hill_name.upper(), k_point_metres), 1, BLACK)
			DISPLAYSURF.blit(text, (40, WINDOWHEIGHT-100))
			text = font.render("{0}'S TURN!".format(player_name.upper()), 1, BLACK)
			DISPLAYSURF.blit(text, (40, WINDOWHEIGHT-70))
			# update and draw wind
			W = (max(min(W[0]+0.05*(random.random()-0.5), 1),-1),max(min(W[1]+0.05*(random.random()-0.5), 1),-1))
			if vector_len(W)>1:
				col = RED
			else:
				col = GREEN
			text = font.render('WIND: {0}'.format("%.1f" % (5.4*vector_len(W))), 1, BLACK)
			DISPLAYSURF.blit(text, (670, 5))
			pygame.draw.rect(DISPLAYSURF, GRAY, [690, 30, 50, 50])
			pygame.draw.line(DISPLAYSURF, col, [715, 55], [715-W[0]*20,55+W[1]*20], 3)
			
		pygame.display.update()			  
		FPSCLOCK.tick(FPS)
	
	

def draw_menu():
	#modes = ['WORLD CUP', 'HILLRECORDS', ]
	DISPLAYSURF.fill(RED)
	
	

def draw_hill_from_file(f,bg, k_point, W):
	DISPLAYSURF.fill(WHITE)
	DISPLAYSURF.blit(bg, (-CameraX,-CameraY)) 
	for i in range(len(f)):
		pygame.draw.line(DISPLAYSURF, ORANGE, (i-CameraX,WINDOWHEIGHT*10-CameraY), (i-CameraX,f[i]-CameraY))
	
	pygame.draw.line(DISPLAYSURF, BLUE, [k_point-CameraX,int(f[k_point])-CameraY],[k_point-200-CameraX,int(f[k_point-200])-CameraY],5)
	for i in range(100):
		pygame.draw.line(DISPLAYSURF, RED,  [k_point+i+1-CameraX,int(f[k_point+i+1])-CameraY],[k_point+i-CameraX,int(f[k_point+i])-CameraY],5)
	
	text = font.render('WIND: {0}'.format("%.1f" % (5.4*vector_len(W))), 1, BLACK)
	DISPLAYSURF.blit(text, (670, 5))
	pygame.draw.rect(DISPLAYSURF, GRAY, [690, 30, 50, 50])
	pygame.draw.line(DISPLAYSURF, GREEN, [715, 55], [715-W[0]*20,55+W[1]*20], 3)


def update_jumper(r,v,a,dt,theta,W): # ,dt,theta
	#TODO check the alpha calculation
	try:
		alpha = math.pi-math.atan(v[1]*v[0]**-1)-(0.5*math.pi+2*math.pi*theta*360**-1)
	except ZeroDivisionError:
		alpha = math.pi*0.5
	#print math.cos(alpha)
	a = (a[0]-0.8*C*v[0]*math.cos(alpha)+W[0]*wind_coeff,max(a[1]-C*v[1]*math.cos(alpha)+W[1]*wind_coeff, 0)) # +C*V[0]**2
	v = (max(v[0]+dt*a[0],1),v[1]+dt*a[1])
	r = (r[0]+dt*v[0], r[1]+dt*v[1])
	return r,v,a

def accelerate(r,v,a,f,dt):
	v = (v[0]+dt*a[1],0) # TODO this is plain wrong, maybe calculate with lagrangian?
	r = (r[0]+dt*v[0], f[int(r[0])])
	return r,v

def deaccelerate(r,v,f,dt):
	v = (max(v[0],30),0)
	r = (min(r[0]+dt*v[0], MAXWIDTH), f[int(r[0])])
	return r,v


def jump(r,v):
	jumpcoeff = jump_window*0.5-abs(r[0]-(imax-jump_window*0.5)) # this calculates the coefficent to strengthen the jump
	v = (v[0], -0.8*max(jumpcoeff,3)) # jump gives velocity in y-direction #TODO check that every hill has no bug of jumping too early leading to landing way too early
	return v, jumpcoeff
	

def telemark(r, f, theta):
	if f[int(r[0])]-r[1]<telemark_margin: # telemark needs a few meters above ground to prepare
		return -1
	ran_num = random.random()
	if 0.5*ran_num>(theta+1)*(len(thetas))**-1: # telemark is succesful only if the jumper is in upper position
		return -1
	return 2

def vector_len(v):
	return math.sqrt(v[0]**2+v[1]**2)

def referee_points(jumpcoeff, landing_style):
	if landing_style==-1:
		return 0.5*int(16-4*random.random())
	elif landing_style==1:
		return min(0.5*int(33-4*random.random()+min(jumpcoeff*random.random(),4)),20)
	elif landing_style==2:
		return min(0.5*int(39-2.1*random.random()+min(jumpcoeff*random.random(),0.8)),20)


def load_hill(name):
	hill_file = open('etc/bg/{0}.txt'.format(name),'r')
	lines = hill_file.readlines()
	hill_file.close()
	f = []
	o = []
	l = []
	
	k_point = float(lines[0]) 
	k_point = int(k_point)
	imax = float(lines[1]) 
	lines = lines[2:]
	for i in range(len(lines)/2):
		f.append(float(lines[i]))
		
	for i in range(len(lines)/2):
		o.append(float(lines[i+len(lines)/2]))
	
	return k_point, imax, f, o
		
	
def calc_len_list(f, imax):
	l = []
	for i in range(int(imax)):
		l.append(0)
	for i in range(len(f)-int(imax)):
		l.append(l[-1]+math.sqrt(1+(f[i+int(imax)]-f[i+int(imax)-1])**2))
	return l
	
	
	

if __name__ == '__main__':
    main()



### plan

#1. make the screen move
#1.1 new images - standardized size
#1.2 HILLS - should the shape be defined pixel by pixel? 
#   3 files basically: background, profile and other parameters(namely maxwidth) and a updateable hill record file with length and name on it 

#4. menu and playmodes
