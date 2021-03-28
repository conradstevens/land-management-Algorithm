"""
Planter that moves and makes decisions in the land
"""
import Pice
from Planter.Vision import Vision


class Planter:
    def __init__(self, bagSize: int, viwDistance: int, pice: Pice):
        """
        Planter must be assigned a pice. this is done in the pice class
        """
        self.vision = Vision(viwDistance)
        self.pice = pice
        self.bagSize, self.bagCount = bagSize, bagSize
        self.x, self.y = 0, 0
        self.finished = False

    def move(self, nx: int, ny: int):
        """
        Moves the planter x+nx, y+ny
        """
        isDead = self.getDead()

        self.x += nx
        self.y += ny

        self.bagUp()
        self.getView()

        self.pice.windw.drawChar('☻', self.x, self.y)  # Note does not update the pice
        self.pice.windw.drawChar(self.pice.piceMatrix[self.y - ny][self.x - nx].char, self.x - nx, self.y - ny, isDead)

    def getView(self):
        """
        Gets the planters view
        """
        # Updates the planter view
        for v in self.vision.visionCircle:
            vx, vy = v[0] + self.x, v[1] + self.y
            if not (vx == self.x and vy == self.y) and \
                    (self.pice.height > vy >= 0) and \
                    (len(self.pice.piceMatrix[vy]) > vx >= 0):

                visionTile = self.getTile(vx, vy)
                if not visionTile.isSeen:
                    self.pice.drawChar(visionTile.char, vx, vy)
                    visionTile.isSeen = True

    def plant(self):
        """
        Plants a tree in the space you are under
        """
        if self.pice.piceMatrix[self.y][self.x].isPlantable:
            self.bagCount -= 1
            self.pice.piceMatrix[self.y][self.x].char = 'T'
            self.pice.piceMatrix[self.y][self.x].isPlantable = False
        else:
            self.pice.piceMatrix[self.y][self.x].dead = True


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

    def getDead(self):
        """
        Determines if move was a dead walk
        """
        if self.pice.piceMatrix[self.y][self.x].dead:
            return 'red'
        return None

