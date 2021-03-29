"""
PlanterClasses that moves and makes decisions in the land
"""
from PiceClasses.Pice import Pice
from PlanterClasses.Vision import Vision


class Planter:
    def __init__(self, bagSize: int, viwDistance: int, pice: Pice):
        """
        PlanterClasses must be assigned a pice. this is done in the pice class
        """
        self.vision = Vision(viwDistance)
        self.pice = pice
        self.bagSize, self.bagCount = bagSize, bagSize
        self.x, self.y = 0, 0
        self.finished = False
        self.noWalk = 0

    def move(self, nx: int, ny: int):
        """
        Moves the planter x+nx, y+ny
        """
        isDead = self.getDead()

        if self.pice.piceMatrix[self.y + ny][self.x + nx].isWalkable:
            self.x += nx
            self.y += ny

            self.bagUp()
            self.getView()

            self.pice.drawChar('☻', self.x, self.y)  # Note does not update the pice
            self.pice.drawChar(self.pice.piceMatrix[self.y - ny][self.x - nx].char, self.x - nx, self.y - ny, isDead)
            self.noWalk = 0
        else:
            self.noWalk += 1
            if self.noWalk > 5:
                self.finished = True


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
            self.pice.piceMatrix[self.y][self.x].isPlanted = True

        else:
            self.pice.piceMatrix[self.y][self.x].isDead = True

    def bagUp(self):
        """
        PlanterClasses fills up their bags if at the cash
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
        if self.pice.piceMatrix[self.y][self.x].isDead:
            return 'red'
        return None


class PlanterAI(Planter):
    """
    Planter with additional AI features
    """

    def __init__(self, bagSize: int, viwDistance: int, pice: Pice):
        super().__init__(bagSize, viwDistance, pice)

    def move(self, nx: int, ny: int):
        super(PlanterAI, self).move(nx, ny)
