from Pice.Window import Windw


class Pice:
    """
    Keeps track of what is in the pice and updates and draws the pice
    """
    filename = -1
    name = -1
    win = -1
    width = 0
    height = 0
    piceMatrix = []
    windw = Windw(-1)

    def __init__(self, windw: Windw, filename: str):
        self.filename = filename
        self.loadPiceMatrix()
        self.windw = windw



    def __str__(self):
        for row in self.piceMatrix:
            for char in row:
                print(char, end='')
            print('')

    def loadPiceMatrix(self):
        """
        Loads the pice matrix
        :return:
        """
        pice = open(self.filename, 'r')

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