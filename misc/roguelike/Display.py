import pygame
import numpy as np

class Color:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 255)
    ORANGE = (255, 140, 0)
    BROWN = (139, 69, 19)
    GRAY = (128,128,128)
 
class Screen:

    def __init__(self, msgBus, width, height, caption, xgrid, ygrid):
        self.messagebus = msgBus
        self.width = width
        self.height = height
        self.xgrid = xgrid
        self.ygrid = ygrid
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.font.init()
        pygame.display.set_caption(caption)
        self.F = pygame.font.SysFont('monospace',20)
        self.renderObjs = [] # list of dicts with keys: char, color, pos
        self.chars = {}
        self.initializeChars()

    def initializeChars(self):
        self.chars['PLAYER'] = self.F.render('@', False, Color.WHITE)
        self.chars['WALL'] = self.F.render('#',False,Color.ORANGE)
        self.chars['FLOOR'] = self.F.render('.',False,Color.GRAY)
        self.chars['DOORCLOSED'] = self.F.render('+',False,Color.BROWN)
        self.chars['DOOROPEN'] = self.F.render('/',False,Color.BROWN)

    def updateObjectList(self, objList):
        self.renderObjs = objList

    def draw(self, charID, pos): # Draw objects and characters
        drawObj = self.chars[charID]
        self.screen.blit(drawObj,(pos[0]*self.xgrid, pos[1]*self.ygrid))

    def update(self): # Update screen
        self.screen.fill(Color.BLACK)
        skipPos = []
        for obj in self.renderObjs:
            self.draw(obj.charID, obj.position)
            skipPos.append(obj.position)
        for x in np.arange(0,self.width/self.xgrid, 1):
            for y in np.arange(0,self.height/self.ygrid, 1):
                if not [x,y] in skipPos:
                    self.draw('FLOOR',[x,y])
        pygame.display.flip()

    def handleMessage(self, msg):
        newMsg = None # Message to be sent out
        if msg.content['type'] is 'update':
            self.updateObjectList(msg.content['objList'])
            self.update()
