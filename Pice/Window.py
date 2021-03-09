import graphics as gr
import time as tm


class Windw:
    """
    Draws and updates the pice window/screen
    """
    fontSizeX = -1
    fontSizeY = -1
    win = None

    def __init__(self, fontSizeX, fontSizeY):
        self.fontSizeX = fontSizeX
        self.fontSizeY = fontSizeY

    def drawWindw(self, width, height):
        """
        Draws Window for the first time
        :param width:
        :param height:
        :return:
        """
        self.win = gr.GraphWin('Planting Lang Management', width * self.fontSizeX + 20, height * self.fontSizeY + 20)
        self.win.setBackground('black')

    def drawChar(self, char: str, x: int, y: int, clr=None):
        """
        Draws char wher spesified
        :param char: str
        :param x: int
        :param y: int
        :param clr: str
        :return:None
        """
        if clr is None:
            clr = getDrawColor(char)

        labelBox = gr.Text(gr.Point((x + 1) * self.fontSizeX, (y + 1) * self.fontSizeY), '█')
        labelBox.setTextColor('black')
        labelBox.draw(self.win)

        labelBox = gr.Text(gr.Point((x + 1) * self.fontSizeX, (y + 1) * self.fontSizeY), char)
        labelBox.setTextColor(clr)
        labelBox.draw(self.win)


def getDrawColor(ch: str):
    """
    Gets the color of the string that is to be drawn
    :param ch:
    :return: str
    """
    if ch == 'T':
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
