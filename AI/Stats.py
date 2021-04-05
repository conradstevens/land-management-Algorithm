from PiceClasses.Window import Windw


class Stats:
    """ Keeps track and displays all the stats of the ai"""

    def __init__(self, window: Windw = None):
        self.highScore, self.piceScore, self.deadCount, self.coveredLand, self.nGames = 1000, 0, 0, 0, 0
        self.window = window


    def updateStats(self, highScore=None, piceScore=None, deadCount=None, coveredLand=None, nGames=None):
        """
        Updates the states of the pice
        """
        if not highScore is None:
            self.highScore = highScore
            self._drawStat('High Score', str(self.highScore), 1, 1)
        if not piceScore is None:
            self.piceScore = piceScore
            self._drawStat('Pice Score', str(self.piceScore), 1, 2)
        if not deadCount is None:
            self.deadCount = deadCount
            self._drawStat('Dead Walks', str(self.deadCount), 2, 2)
        if not coveredLand is None:
            self.coveredLand = coveredLand
            self._drawStat('Covered Land', str(self.coveredLand), 2, 1)
        if not nGames is None:
            self.nGames = nGames
            self._drawStat('Game Number', str(self.piceScore), 1, 3)
        self.drawStats()

    def drawStats(self):
        """
        draws all the stats
        """
        if not self.window is None:
            self._drawStat('High Score', str(self.highScore), 1, 1)
            self._drawStat('Pice Score', str(self.piceScore), 1, 2)
            self._drawStat('Game Number', str(self.piceScore), 1, 3)
            self._drawStat('Covered Land', str(self.coveredLand), 2, 1)
            self._drawStat('Dead Walks', str(self.deadCount), 2, 2)

    def _drawStat(self, title: str, stat: str, bX: int, bY: int, textlen=22):
        """"
        loads a stat onto the screen
        bx: bottom x
        by: bottom y
        """
        titleStr = title + ': '
        textStr = titleStr + stat

        while len(textStr) < 16:
            titleStr = titleStr + ' '
            textStr = titleStr + stat

        self.window.drawChar(textStr, (bX - 1) * 7 + 2, self.window.piceH + bY, 'white', fontSize=9)
