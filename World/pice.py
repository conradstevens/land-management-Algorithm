from World.window import Windw


class Pice:
    """
    Keeps track of what is in the pice and updates and draws the pice
    """

    def __init__(self, fileName: str):
        self.fileName = fileName
        self.piceMatrix = []
        self.width, self.height = self.loadPiceMatrix(fileName)
        self.window = None

    def __str__(self):
        for row in self.piceMatrix:
            for char in row:
                print(char, end='')
            print('')

    def loadPiceMatrix(self, filename: str):
        """
        Loads the pice matrix
        """
        pice = open(filename, 'r')
        line = pice.readline()
        charY = -1
        height, width = 0, 0

        while line != '':
            height += 1
            charY += 1
            rowWidth = -1
            matrixLine = []

            for charX in range(0, len(line) - 1):
                rowWidth += 1
                tile = Tile(charX, charY, line[charX])
                matrixLine.append(tile)

            self.piceMatrix.append(matrixLine)
            line = pice.readline()

            if width < rowWidth:
                width = rowWidth
        return width, height

    def findChar(self, char):
        """
        Returns the coordinates of where the pice is
        :return: List
        """
        for r in self.piceMatrix:
            for c in r:
                if c.char == char:
                    return c.x, c.y

    def updateTile(self, char: str, x: int, y: int, clr=None):
        """
        Updates the text of one element in teh pice
        """
        self.piceMatrix[y][x].char = char
        self.drawChar(char, x, y, clr)

    def drawChar(self, char, x, y, clr=None):
        pass

    def terminate(self):
        """ Terminates window if has one"""
        pass


class PiceWind(Pice):
    """"
    File to run make the pice so it can also be seen
    """
    def __init__(self, fileName: str, font: float):
        super().__init__(fileName)
        self.window = Windw(fontSizeX=20, fontSizeY=20, width=self.width, height=self.height)
        self.drawPice()

    def drawPice(self):
        """
       Draws the pice for the first time
       :return: None"""
        self.window.drawWindw(self.width, self.height)
        for r in self.piceMatrix:
            for c in r:
                self.window.drawChar(c.char, c.x, c.y, clr='blue')

    def drawChar(self, char, x, y, clr=None):
        """
        Draws the character in the window
        """
        self.window.drawChar(char, x, y, clr=clr)

    def terminate(self):
        """ Terminates window if has one"""
        self.window.terminate()


class Tile:
    isSeen = False
    isPlantable = False
    isPlanted = False
    isDead = False
    isWalkable = True

    def __init__(self, x, y, char):
        self.x, self.y, = x, y
        self.char = char

        if char == '.':
            self.isPlantable = True
        elif char == 'X':
            self.isWalkable = False
