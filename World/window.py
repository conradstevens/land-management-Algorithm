import graphics as gr
import time as tm


class Windw:
    """
    Draws and updates the pice window/screen
    """

    def __init__(self, fontSizeX, fontSizeY, width, height):
        self.fontSizeX, self.fontSizeY = fontSizeX, fontSizeY
        self.piceW, self.piceH = width, height  # In Tiles
        self.windowW, self.windowH = max(300, width * self.fontSizeX + 30), (height * self.fontSizeY + 100)

    def drawWindw(self, width, height):
        """
        Draws Window for the first time
        :param width:
        :param height:
        :return:
        """
        self.win = gr.GraphWin('Planting Lang Management', self.windowW, self.windowH)
        self.win.setBackground('black')

    def drawChar(self, char: str, x: int, y: int, clr=None, fontSize=None):
        """
        Draws char wher spesified
        """
        if clr is None:
            clr = self._getDrawColor(char)

        self.erase(x, y)
        labelBox = gr.Text(gr.Point((x + 1) * self.fontSizeX, (y + 1) * self.fontSizeY), char)
        labelBox.setTextColor(clr)

        if not fontSize is None:
            labelBox.setSize(fontSize)
            labelBox.setFace('courier')
            labelBox.draw(self.win)
        else:
            labelBox.setSize(12)
            labelBox.draw(self.win)

    def erase(self, x, y, clr='black'):
        """ Draws a black square"""
        labelBox = gr.Text(gr.Point((x + 1) * self.fontSizeX, (y + 1) * self.fontSizeY), '█')
        labelBox.setTextColor(clr)
        labelBox.draw(self.win)

    def _getDrawColor(self, ch: str):
        """
        Gets the color of the string that is to be drawn
        :param ch:
        :return: str
        """
        if ch == '-':
            return 'pink3'
        if ch == 'T':
            return 'green2'
        if ch == '■':
            return 'green2'
        if ch == 'D':
            return 'red'
        if ch == 'C':
            return 'pink3'
        if ch == '?':
            return 'yellow'
        if ch == '☻':
            return 'yellow'
        return 'white'

    def terminate(self):
        """ Closes the window """
        self.win.close()
