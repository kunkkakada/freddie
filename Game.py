from Message import *
from Input import *
import pygame

class Game:
	
	def __init__(self):
		self.msg_bus = MessageBus()
		self.systems = {'Input': Input(self.msg_bus)}
		self.screen = pygame.display.set_mode((800, 600))
		#self.audio = audio()
		#self.gui = gui()
		#self.scene = scene() # basically this is one level; it holds ais, world, player, npcs
		#self.gamelogic = gamelogic()
		
		#self.renderer = renderer()
	
	def loop(self):
		running = True
		
		while running:
			events = pygame.event.get()
			keys = pygame.key.get_pressed()
			
			for event in events:
				if event.type == MOUSEMOTION:
					self.systems['Input'].handle_mouse(0, event.buttons, pygame.mouse.get_pos(), pygame.mouse.get_rel())
				elif event.type == MOUSEBUTTONUP:
					self.systems['Input'].handle_mouse(1, event.button, pygame.mouse.get_pos())
				elif event.type == MOUSEBUTTONDOWN:
					self.systems['Input'].handle_mouse(2, event.button, pygame.mouse.get_pos())
				elif event.type == KEYDOWN:
					self.systems['Input'].handle_key_down(event.key)
				elif event.type == KEYUP:
					self.systems['Input'].handle_key_up(event.key)
					
			self.msg_bus.print_message_bus()
			self.clean_message_bus()
			
			
			
			pygame.event.pump()
			pygame.time.wait(50)
		
		#while gamelogic.running:
			# get input, and append messages accordingly
			#input.get() # ->messages to bus
			#cleanmessagebus
			
			#scene.update ->messages to bus
			#cleanmessagebus
			
			#audio.play()
			#renderer.draw()
			#gui.update()
	
	def clean_message_bus(self):
		# send messages out from the messagebus to correct receivers
		while len(self.msg_bus.msg_list)>0:
			# select correct system depending on the message type, handle message and remove from bus
			msg = self.msg_bus.msg_list.pop(0)
			for system in self.systems.values():
				system.handle_message(msg)
	

if __name__=='__main__':
	pygame.init()
	game = Game()
	game.loop()
