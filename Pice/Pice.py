from Pice.Window import Windw


class Pice:
    """
    Keeps track of what is in the pice and updates and draws the pice
    """
    filename = -1
    name = -1
    win = -1
    piceMatrix = []

    def __init__(self, window: Windw, filename: str):
        self.filename = filename
        self.loadPiceMatrix()

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
            matrixLine = []
            for char in line[0: len(line) - 1]:
                matrixLine.append(char)
            self.piceMatrix.append(matrixLine)
            line = pice.readline()

    # def drawPice(self):
    #    """
    #    Draws the pice for the first time
    #    :return: Na """
    #    #for row in self.piceMatrix:
