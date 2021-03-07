from Pice.Window import Windw


class Pice:
    """
    Keeps track of what is in the pice and updates and draws the pice
    """
    name = -1
    win = -1
    width = 0
    height = 0
    piceMatrix = []
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
        self.windw = windw
        pice = open(filename, 'r')

        line = pice.readline()
        while line != '':
            self.height += 1
            rowWidth = 0
            matrixLine = []

            for char in line[0: len(line) - 1]:
                rowWidth += 1
                matrixLine.append(char)

            self.piceMatrix.append(matrixLine)
            line = pice.readline()

            if self.width < rowWidth:
                self.width = rowWidth

    def drawPice(self):
        """
       Draws the pice for the first time
       :return: None"""
        self.windw.drawWindw(self.width, self.height)
        rCount = 0
        cCount = 0
        for r in self.piceMatrix:
            for c in r:
                self.windw.drawChar(c, cCount, rCount)
                cCount += 1
            cCount = 0
            rCount += 1

    def placePlaner(self, planter):
        """
        places the planter in the pice
        :return: None
        """
        coordinates = self.findChar('C')
        self.updateTile('☻', coordinates[0], coordinates[1])

        # Assigns the planter Pice information
        planter.x, planter.y = coordinates[0], coordinates[1]
        planter.underTile = 'C'
        planter.pice = self

    def findChar(self, char):
        """
        Returns the coordinates of where the pice is
        :return: List
        """
        rCount = 0
        cCount = 0
        for r in self.piceMatrix:
            for c in r:
                if c == char:
                    return [cCount, rCount]
                cCount += 1
            cCount = 0
            rCount += 1

    def updateTile(self, char: str, x: int, y: int, clr=None):
        """
        Updates the text of one element in teh pice
        :return: None
        """
        if char is None or len(char) > 1:
            print("Warning Char > 1")

        self.piceMatrix[y][x] = char
        self.windw.drawChar(char, x, y, clr)
