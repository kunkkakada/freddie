import itertools
import numpy as np
from Object import *

class Scene:

    def __init__(self, msgBus):
        self.messageBus = msgBus
        self.objects = {}
        self.characters = {}

    def addObject(self, obj):
        if obj.charID.lower() == 'player':
            obj.objID = 'player'
        else:
            obj.objID = itertools.count().next
        self.objects[obj.objID] = obj

    def addRoom(self, upperLeftCorner, widthRight, heightDown, doorFlag, doorPos):
        # Doorflag = 0 -> hole, 1 -> closed door, 2 -> open door
        for posX in range(upperLeftCorner[0], upperLeftCorner[0]+widthRight+1):
            for posY in range(upperLeftCorner[1],upperLeftCorner[1]+heightDown+1):
                if posY == upperLeftCorner[1] or posY == upperLeftCorner[1]+heightDown or posX == upperLeftCorner[0] or posX == upperLeftCorner[0]+widthRight:
                    if [posX, posY] == doorPos:
                        if doorFlag != 0:
                            door = Door(doorPos)
                            if doorFlag == 2:
                                door.openDoor()
                            self.addObject(door)
                    else:
                        self.addObject(Wall([posX,posY]))

    def checkCollision(self,pos):
        # Return 1 if collision, 0 if no collision
        for obj in self.objects.values():
            if obj.position == pos and obj.block == 1:
                return 1
        return 0

    def handleMessage(self, msg):
            obj = self.objects[msg.content['objID']]
            if msg.content['action'] == 'move':
                newPos = np.add(np.array(obj.position),np.array(msg.content['param'])).tolist()
                if self.checkCollision(newPos) == 0:
                    obj.move(msg.content['param'])
                else:
                    print "Oof!"


