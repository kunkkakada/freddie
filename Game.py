from Message import *
from Input import *

class Game(object):
	
	def __init__(self):
		self.messageBus = []
		#self.audio = Audio()
		#self.gui = GUI()
		#self.scene = Scene() # basically this is one level; it holds AIs, world, player, NPCs
		#self.gameLogic = GameLogic()
		#self.inputHandler = Input()
		#self.renderer = Renderer()

	def loop(self):
		
		#while gameLogic.running:
			# get input, and append messages accordingly
			#Input.get() # ->messages to Bus
			#cleanMessageBus
			
			#scene.update ->messages to Bus
			#cleanMessageBus
			
			#audio.play()
			#renderer.draw()
			#gui.update()
			
		
		
    def clean_message_bus(self):
        # Send messages out from the messagebus to correct receivers
        while len(self.msg_list)>0:
            # Select correct system depending on the message type, handle message and remove from bus
            msg = self.msg_list.pop(0)
            system = self.systems[msg.msg_type]
            system.handle_message(msg)
