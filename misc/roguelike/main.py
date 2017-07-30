import pygame
import numpy as np

from Message import *
from Input import *
from Char import *
from Object import *
from Display import *
from Scene import *

pygame.init()

# Initialize MessageBus
msgBus = MessageBus() 

# Initialize systems
inputHandler = Input(msgBus)
scene = Scene(msgBus)
screen = Screen(msgBus, 800, 600, 'Roguelike', 10, 20)

# Define function for loading scenes from predefined text files
def loadScene(scenefile):
    scene = Scene(msgBus)
    file = open(scenefile, "r")
    for line in file:
        exec(line)
        #obj = eval(line)
        #scene.addObject(obj)
    file.close
    return scene

# Load scene
scene1 = loadScene("map1.txt")

# Initialize system list
msgBus.systems[MsgType.INPUT] = inputHandler
msgBus.systems[MsgType.SCENE] = scene1
msgBus.systems[MsgType.SCREEN] = screen

# Message to SCREEN: Update screen before main loop starts
msg = Message(MsgType.SCREEN)
msg.content = {'type': 'update', 'objList': scene1.objects.values()}
msgBus.postMessage(msg)
screen.updateObjectList(scene1.objects.values())

# Clean message bus
msgBus.cleanMessageBus()

# Set repeating keys on
pygame.key.set_repeat(1,125)

# Main loop
is_running = True
while is_running:
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Message to INPUT: Key pressed down
            msg = Message(MsgType.INPUT)
            msg.content = {'type': 'keydown', 'key': event.dict['key']} # Send keydown as 
            msgBus.postMessage(msg)

            # Clean message bus
            msgBus.cleanMessageBus()

            # Message to SCREEN: Update screen
            msg = Message(MsgType.SCREEN)
            msg.content = {'type': 'update', 'objList': scene1.objects.values()}
            msgBus.postMessage(msg)
            
            # Clean message bus
            msgBus.cleanMessageBus()
            
        if event.type == pygame.QUIT:
            is_running = False

pygame.quit()
