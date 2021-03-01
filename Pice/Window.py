import graphics as gr


class Windw:
    """
    Draws and updates the pice window/screen
    """
    def __init__(self, abc):
        win = gr.GraphWin('Planting Lang Management', 100, 100)
        win.setBackground('black')
