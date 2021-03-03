import graphics as gr


class Windw:
    """
    Draws and updates the pice window/screen
    """
    fontSize = -1

    def __init__(self, fontSize):
        self.fontSize = fontSize

    def drawWindw(self, width, height):
        """
        Draws Window for the first time
        :param width:
        :param height:
        :return:
        """
        print(width)
        print(height)
        win = gr.GraphWin('Planting Lang Management', width*self.fontSize, height*self.fontSize)
        win.setBackground('black')
        print(width*self.fontSize)
        print(height*self.fontSize)

