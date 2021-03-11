"""
Planter that moves and makes decisions in the land
"""
from Pice.Pice import Pice
from Planter.Vision import Vision
from Pice.Tile import Tile

class Planter:
    pice = Pice()
    bagSize = -1
    bagCount = -1
    underTile = '-1'
    piceMemory = []
    x, y, = -1, -1
    finished = False
    vision = Vision(1)
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
        self.x += nx
        self.y += ny

        self.markDead()
        self.bagUp()
        self.getView()

        self.pice.windw.drawChar('☻', self.x, self.y)  # Note does not update the pice
        # At End for smoothest animation transition
        self.pice.windw.drawChar(self.pice.piceMatrix[self.y - ny][self.x - nx].char, self.x - nx, self.y - ny)


    def getView(self):
        """
        Gets the planters view
        """
        # Updates the plater view
        for v in self.vision.visionCircle:
            vx, vy = v[0] + self.x, v[1] + self.y
            if not (vx == self.x and vy == self.y) and \
                    (self.pice.height > vy >= 0) and \
                    (len(self.pice.piceMatrix[vy]) > vx >= 0):

                visionTile = self.getTile(vx, vy)
                if not visionTile.isSeen:
                    self.pice.windw.drawChar(visionTile.char, vx, vy)
                    visionTile.isSeen = True

    def plant(self):
        """
        Plants a tree in the space you are under
        """
        if self.pice.piceMatrix[self.y][self.x].char == '.':
            self.bagCount -= 1
            self.pice.piceMatrix[self.y][self.x].char = 'T'
            self.pice.piceMatrix[self.y][self.x].isPlantable = False

    def bagUp(self):
        """
        Planter fills up their bags if at the cash
        """
        if self.getUderTile().char == 'C':
            self.bagCount = self.bagSize

    def getUderTile(self):
        """
        Get's the tile the planter is on
        :return:
        :rtype:
        """
        return self.pice.piceMatrix[self.y][self.x]

    def checkVision(self, nx, ny):
        """
        Returns the character of the vision tile checked
        :return: the tiele being looked at
        """
        visionTile = self.pice.piceMatrix[self.y + ny][self.x + nx]
        if visionTile.isSeen:
            return visionTile
        return None

    def getTile(self, nx, ny):
        """
        Returns the tile under self + x + y
        :rtype Tile
        """
        return self.pice.piceMatrix[ny][nx]

    def markDead(self):
        """
        Marks move as a deadwalk
        """
        underChar = self.getUderTile().char
        if self.bagCount < 1 and underChar != 'C':
             self.pice.windw.drawChar(underChar, self.x, self.y, 'red')
