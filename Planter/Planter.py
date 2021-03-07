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
        self.pice.updateTile(self.underTile, self.x, self.y)
        self.x += nx
        self.y -= ny
        self.pice.windw.drawChar('☻', self.x, self.y)  # Note does not update the pice

    def getView(self):
        for i in self.vision.visionCircle:
            self.pice.windw.drawChar('G', self.x + i[0], self.y + i[1], clr='red')


    def plantPice(self, algo):
        """
        Planter plants around until planter thinks they are done
        """
        pass



