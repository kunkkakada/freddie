from Message import *
from pygame.locals import *


class Input:
	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
	
	def handle_message(self, msg):
		return
		
	# called from main; keys parameter is the list of booleans from pygame.key.get_pressed()
	def handle_keys(self, keys, state='running'):
		if state=='running':
			if keys[K_f]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'fart'}
				self.msg_bus.post_message(msg)
			
			if keys[K_c]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'curse'}
				self.msg_bus.post_message(msg)
	
			if keys[K_a]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'turn left'}
				self.msg_bus.post_message(msg)
				
			if keys[K_d]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'turn right'}
				self.msg_bus.post_message(msg)
		
			if keys[K_w]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'forward'}
				self.msg_bus.post_message(msg)
	
			if keys[K_s]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'backward'}
				self.msg_bus.post_message(msg)
	
			if keys[K_SPACE]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'jump'}
				self.msg_bus.post_message(msg)
				
			if keys[K_e]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'use'}
				self.msg_bus.post_message(msg)
				
			if keys[K_r]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'reload'}
				self.msg_bus.post_message(msg)
				
			if keys[K_i]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'inventory'}
				self.msg_bus.post_message(msg)
				
			if keys[K_z]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'switch weapon'}
				self.msg_bus.post_message(msg)
				
			if keys[K_ESCAPE]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'menu'}
				self.msg_bus.post_message(msg)
				
			if keys[K_q]:
				msg = Message(MsgType.INPUT)
				msg.content={'type': 'quick use'}
				self.msg_bus.post_message(msg)
	
	
	# the mouse event is translated to int values in main, and here the corresponding messages are posted
	# MOUSEMOTION 0, MOUSEBUTTONUP 1, MOUSEBUTTONDOWN 2
	# UP/DOWN: LMB 1, scroll click 2, RMB 3, scroll up 4, scroll down 5
	# MOTION: list of clicked buttons
	def handle_mouse(self, event_type, button, pos, rel=None,  state='running'):
		msg = Message(MsgType.INPUT)
		if state=='running':
			
			if event_type==0:
				msg.content={'type': 'move camera', 'rel': rel}
				
			elif event_type==1:
				if button==1:
					msg.content={'type': 'stop shooting'}
				elif button==3:
					msg.content={'type': 'release throwable'}
					
			elif event_type==2:
				if button==1:
					msg.content={'type': 'shoot'}
				elif button==3:
					msg.content={'type': 'load throwable'}
				elif button==4:
					msg.content={'type': 'switch camera forward'}
				elif button==5:
					msg.content={'type': 'switch camera backward'}
					
		if msg.content:
			self.msg_bus.post_message(msg)
		
