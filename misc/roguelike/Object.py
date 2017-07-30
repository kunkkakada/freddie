from Display import *

class Object(object):

    def __init__self(self):
        self.objID = None
        self.type = None
        self.position = None
        self.block = None
        self.open = None
        self.char = None

class Wall(Object):

    def __init__(self, pos):
        self.position = pos
        self.block = 1
        self.charID = 'WALL'

class Door(Object):

    def __init__(self, pos):
        # Closed by default
        self.position = pos
        self.block = 1
        self.open = 0
        self.charID = 'DOORCLOSED'

    def openDoor(self):
        self.block = 0
        self.open = 1
        self.charID = 'DOOROPEN'

    def closeDoor(self):
        self.block = 1
        self.open = 0
        self.charID = 'DOORCLOSED'


    
