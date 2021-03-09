from Pice.Window import Windw
from Pice.Tile import Tile

class Pice:
    """
    Keeps track of what is in the pice and updates and draws the pice
    """
    name = -1
    win = -1
    width = 0
    height = 0
    piceMatrix = [[Tile]]
    windw = Windw(-1, -1)

    def __str__(self):
        for row in self.piceMatrix:
            for char in row:
                print(char, end='')
            print('')

    def loadPiceMatrix(self, windw: Windw, filename: str):
        """
        Loads the pice matrix
        :return:
        """
        self.piceMatrix = []
        self.windw = windw
        pice = open(filename, 'r')

        line = pice.readline()
        charY = -1
        while line != '':
            self.height += 1
            charY += 1
            rowWidth = -1
            matrixLine = []

            for charX in range(0, len(line) - 1):
                rowWidth += 1
                tile = Tile(charX, charY, line[charX])
                matrixLine.append(tile)

            self.piceMatrix.append(matrixLine)
            line = pice.readline()

            if self.width < rowWidth:
                self.width = rowWidth

    def drawPice(self):
        """
       Draws the pice for the first time
       :return: None"""
        self.windw.drawWindw(self.width, self.height)
        for r in self.piceMatrix:
            for c in r:
                self.windw.drawChar(c.char, c.x, c.y)

    def placePlaner(self, planter):
        """
        places the planter in the pice
        :return: None
        """
        coordinates = self.findChar('C')

        # Assigns the planter Pice information
        planter.x, planter.y = coordinates[0], coordinates[1]
        self.windw.drawChar('☻', planter.x, planter.y)
        planter.pice = self

    def findChar(self, char):
        """
        Returns the coordinates of where the pice is
        :return: List
        """
        for r in self.piceMatrix:
            for c in r:
                if c.char == char:
                    return [c.x, c.y]

    def updateTile(self, char: str, x: int, y: int, clr=None):
        """
        Updates the text of one element in teh pice
        :return: None
        """
        self.piceMatrix[y][x].char = char
        self.windw.drawChar(char, x, y, clr)