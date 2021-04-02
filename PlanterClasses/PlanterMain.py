"""
PlanterClasses that moves and makes decisions in the land
"""
from PiceClasses.Pice import Pice
from PiceClasses.Pice import Tile
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
        self.noWalk = 0

        self.finished = False
        self.deadCount = 0

        self.placePlanter()

    def move(self, nx: int, ny: int, plant: bool):
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
            self.pice.drawChar(self.getTile(-nx, -ny, selfRelative=True).char, self.x - nx, self.y - ny, isDead)
            self.noWalk = 0
        else:
            self.noWalk += 1
            if self.noWalk > 5:
                self.finished = True

        if plant:
            self.plant()
        else:
            self.getUderTile().isDead = True
            self.deadCount += 1

    def getView(self):
        """
        Gets the planters view
        """
        # Updates the planter view
        for v in self.vision.visionCircle:
            vx, vy = v[0], v[1]
            tile = self.getTile(nx=vx, ny=vy, selfRelative=True)

            #  vx, vy = v[0] + self.x, v[1] + self.y
            #  if not (vx == self.x and vy == self.y) and \
            #          (self.pice.height > vy >= 0) and \
            #          (len(self.pice.piceMatrix[vy]) > vx >= 0):
            # visionTile = self.getTile(vx, vy)

            if tile is not None and not tile.isSeen:
                self.pice.drawChar(tile.char, vx, vy)
                tile.isSeen = True

    def plant(self):
        """
        Plants a tree in the space you are under
        """
        if self.getUderTile().isPlantable and self.bagCount > 0:
            self.bagCount -= 1
            self.getUderTile().char = 'T'
            self.getUderTile().isPlantable = False
            self.getUderTile().isPlanted = True

        else:
            self.getUderTile().isDead = True

    def placePlanter(self):
        """
        Places the planter at the cash of the pice
        """
        x, y = self.pice.findChar('C')
        self.x, self.y = x, y
        self.pice.drawChar('☻', x, y)
        self.getView()

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
        :rtype: Tile
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

    def getTile(self, nx, ny, selfRelative=False):
        """
        Returns the tile under self + x + y
        :rtype Tile
        """
        if selfRelative:
            return self.getTile(self.x + nx, self.y + ny, selfRelative=False)

        try:
            return self.pice.piceMatrix[ny][nx]
        except IndexError:
            return None

    def getDead(self):
        """
        Determines if move was a dead walk
        """
        if self.pice.piceMatrix[self.y][self.x].isDead:
            self.deadCount += 1
            return 'red'
        return None
