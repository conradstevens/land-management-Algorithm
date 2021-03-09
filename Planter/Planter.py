"""
Planter that moves and makes decisions in the land
"""
from Pice.Pice import Pice
from Planter.Vision import Vision

class Planter:
    pice = Pice()
    bagSize = -1
    underTile = '-1'
    piceMemory = []
    x, y, = -1, -1
    finished = False
    vision = Vision(1)
    view = []

    def __init__(self, bagSize: int, viwDistance: int):
        """
        Planter must be assigned a pice. this is done in the pice class
        """
        self.bagSize = bagSize
        self.vision = Vision(viwDistance)

    def move(self, nx: int, ny: int):
        """
        Moves the planter x+nx, y+ny
        """
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
                self.pice.windw.drawChar(viewT.get('v').char, viewT.get('x'), viewT.get('y'), clr='blue')

    def plantPice(self, algo):
        """
        Planter plants around until planter thinks they are done
        """
        pass



