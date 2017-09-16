from Message import *
from pygame.locals import *
import Console

class Input:
	def __init__(self, msg_bus):
		self.msg_bus = msg_bus
	
	def handle_message(self, msg):
		return
		
				
# called from main; key parameter is a key from pygame.locals				
	def handle_key_down(self, key, t, state='running'):
		if state=='running':
			if key==K_f:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'fart', 'time':t}
				self.msg_bus.post_message(msg)
			
			if key==K_c:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'curse', 'time':t}
				self.msg_bus.post_message(msg)
	
			if key==K_a:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'turn left', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_d:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'turn right', 'time':t}
				self.msg_bus.post_message(msg)
		
			if key==K_w:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'forward', 'time':t}
				self.msg_bus.post_message(msg)
	
			if key==K_s:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'backward', 'time':t}
				self.msg_bus.post_message(msg)
	
			if key==K_SPACE:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'jump', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_e:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'use', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_r:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'reload', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_i:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'inventory', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_z:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'switch weapon', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_ESCAPE:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'menu', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_q:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'quick use', 'time':t}
				self.msg_bus.post_message(msg)
				
# called from main; key parameter is a key from pygame.locals				
	def handle_key_up(self, key, t, state='running'):
		if state=='running':
			if key==K_f:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'stop fart', 'time':t}
				self.msg_bus.post_message(msg)
			
	
			if key==K_a:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'stop turn left', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_d:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'stop turn right', 'time':t}
				self.msg_bus.post_message(msg)
		
			if key==K_w:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'stop forward', 'time':t}
				self.msg_bus.post_message(msg)
	
			if key==K_s:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'stop backward', 'time':t}
				self.msg_bus.post_message(msg)
	
			if key==K_SPACE:
				msg = Message(MsgType.INPUT)
				msg.content={'cmd': 'stop jump', 'time':t}
				self.msg_bus.post_message(msg)
				
			if key==K_TAB:
				inp = raw_input("Console>\n")
				msg = Console.parse_command(inp)
				if msg is not False:
					self.msg_bus.post_message(msg)
				
	
	# the mouse event is translated to int values in main, and here the corresponding messages are posted
	# MOUSEMOTION 0, MOUSEBUTTONUP 1, MOUSEBUTTONDOWN 2
	# UP/DOWN: LMB 1, scroll click 2, RMB 3, scroll up 4, scroll down 5
	# MOTION: list of clicked buttons
	def handle_mouse(self, event_type, button, pos, t, rel=None,  state='running'):
		msg = Message(MsgType.INPUT)
		if state=='running':
			
			if event_type==0:
				msg.content={'cmd': 'move camera', 'rel': rel, 'time':t}
				
			elif event_type==1:
				if button==1:
					msg.content={'cmd': 'stop shoot', 'time':t}
				elif button==3:
					msg.content={'cmd': 'release throwable', 'time':t}
					
			elif event_type==2:
				if button==1:
					msg.content={'cmd': 'shoot', 'time':t}
				elif button==3:
					msg.content={'cmd': 'load throwable', 'time':t}
				elif button==4:
					msg.content={'cmd': 'switch camera forward', 'time':t}
				elif button==5:
					msg.content={'cmd': 'switch camera backward', 'time':t}
					
		if msg.content:
			self.msg_bus.post_message(msg)
		
