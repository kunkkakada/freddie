import numpy as np
from Display import Color

class Character(object):

    def __init__(self, initPos, charType, name):
        self.objID = None
        self.position = initPos
        self.block = 1
        self.charID = None # ASCII character properties 
        self.type = charType # Player or monster or npc or companion
        self.name = name
        self.id = None

    def move(self, direction):
        # Direction as [dx,dy] list of position change
        pos = np.array(self.position)
        dpos = np.array(direction)
        self.position = np.add(pos,dpos).tolist()

class Player(Character):
    
    def __init__(self, initPos, name):
        Character.__init__(self,initPos, "Player", name)
        self.charID = 'PLAYER'
        #self.inventory = Inventory()
