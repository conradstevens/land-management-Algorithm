"""
Planter that moves and makes decisions in the land
"""
from Pice.Pice import Pice
from Planter.Vision import Vision

class Planter:
    pice = Pice()
    bagSize = -1
    bagCount = -1
    underTile = '-1'
    piceMemory = []
    x, y, = -1, -1
    finished = False
    vision = Vision(1)
    view = []
    piceDone = False

    def __init__(self, bagSize: int, viwDistance: int):
        """
        Planter must be assigned a pice. this is done in the pice class
        """
        self.bagSize, self.bagCount = bagSize, bagSize
        self.vision = Vision(viwDistance)

    def move(self, nx: int, ny: int):
        """
        Moves the planter x+nx, y+ny
        """
        self.pice.windw.drawChar(self.pice.piceMatrix[self.y][self.x].char, self.x, self.y)
        self.x += nx
        self.y -= ny
        self.pice.windw.drawChar('☻', self.x, self.y)  # Note does not update the pice

    def getView(self):
        """
        Gets the planters view
        """
        # Updates the plater view
        self.view = self.vision.getPiceVision(self.x, self.y, self.pice)

        # Updates the plater view
        for viewT in self.view:
            if [viewT.get('x'), viewT.get('y')] != [self.x, self.y]:
                self.pice.piceMatrix[viewT.get('y')][viewT.get('x')].isSeen = True
                self.pice.windw.drawChar(viewT.get('v').char, viewT.get('x'), viewT.get('y'), clr='blue')





