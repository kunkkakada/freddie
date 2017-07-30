from Message import *
import pygame


class Input:

    def __init__(self, msgBus):
        self.messageBus = msgBus

    def handleMessage(self, msg):
        newMsg = None # Message to be sent out
        if msg.content['type'] is 'keydown':
            # Keypress
            if msg.content['key'] == pygame.K_KP6:
                # Move right
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [1,0]}
            if msg.content['key'] == pygame.K_KP4:
                # Move left
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [-1,0]}
            if msg.content['key'] == pygame.K_KP8:
                # Move up
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [0,-1]}
            if msg.content['key'] == pygame.K_KP2:
                # Move down
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [0,1]}
            if msg.content['key'] == pygame.K_KP9:
                # Move NE
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [1,-1]}
            if msg.content['key'] == pygame.K_KP7:
                # Move NW
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [-1,-1]}
            if msg.content['key'] == pygame.K_KP3:
                # Move SE
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [1,1]}            
            if msg.content['key'] == pygame.K_KP1:
                # Move SW
                newMsg = Message(MsgType.SCENE)
                newMsg.content = {'objID': 'player', 'action': 'move', 'param': [-1,1]}
        if newMsg is not None:
            self.messageBus.postMessage(newMsg)
