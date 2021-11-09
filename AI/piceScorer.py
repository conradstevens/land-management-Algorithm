from World.window import Windw
from World.planterMain import Planter


class PiceScore:
    """
    Scores the pice based on what move is best
    TODO add squarness to score
    TODO Maybe reward tree planting - Is this different form peanalizing dead walking?
    TODO reward size of bagups - would incorporate function that optimizes fule use based on weight of trees carried
    """

    def __init__(self, planter: Planter):
        # Logistic Classes
        self.planter, self.pice = planter, planter.pice
        self.scoreDisplay = ScoreDisplay(self.planter.pice.window)
        # Game Scores
        self.oldScore = 0
        self.piceScore = 0
        self.reward = 0
        self.coveredLand = 0
        # Multi Game Scores
        self.highScore = 0
        self.gameNum = 0
        # Consecutive
        self.downStreak = 0

    def scorePice(self):
        """
        :return: score of the pice
        """
        self.oldScore = self.piceScore
        self.piceScore = self.planter.plantCount - self.planter.deadCount
        self.scoreDisplay.updateStats(piceScore=self.piceScore)
        self.reward = self.piceScore - self.oldScore
        self.coveredLand = self.planter.plantCount

        if self.reward >= 1:
            self.scoreDisplay.updateStats(coveredLand=self.coveredLand)
            self.downStreak = 0

        else:
            self.scoreDisplay.updateStats(deadCount=self.planter.deadCount)
            self.downStreak += 1

        if self.piceScore > self.highScore:
            self.highScore = self.piceScore
            self.scoreDisplay.updateStats(highScore=self.highScore)

        return self.reward

    def resetNewPice(self, epoch, planter: Planter):
        """ Resets the game scores """
        self.planter = planter
        self.scoreDisplay.window = planter.pice.window
        self.piceScore, self.reward, self.coveredLand = 0, 0, 0
        self.gameNum = epoch
        self.downStreak = 0
        self.scoreDisplay.updateStats(piceScore=self.piceScore, deadCount=self.planter.deadCount,
                                      coveredLand=self.coveredLand, nGames=self.gameNum,
                                      highScore=max(0, self.highScore))

class ScoreDisplay:
    """ Keeps track and displays all the stats of the ai"""

    def __init__(self, window: Windw = None):
        self.window = window

    def updateStats(self, highScore=None, piceScore=None, deadCount=None, coveredLand=None, nGames=None):
        """
        Updates the states of the pice
        """
        if not highScore is None:
            self._drawStat('High Score', str(highScore), 1, 1)
        if not piceScore is None:
            self._drawStat('Pice Score', str(piceScore), 1, 2)
        if not deadCount is None:
            self._drawStat('Dead Walks', str(deadCount), 2, 2)
        if not coveredLand is None:
            self._drawStat('Covered Land', str(coveredLand), 2, 1)
        if not nGames is None:
            self._drawStat('Game Number', str(nGames), 1, 3)

    def _drawStat(self, title: str, stat: str, bX: int, bY: int, textlen=9):
        """"
        loads a stat onto the screen
        bx: bottom x
        by: bottom y
        """
        if self.window is not None:
            titleStr = title + ': '
            textStr = titleStr + stat

            while len(textStr) < 16:
                titleStr = titleStr + ' '
                textStr = titleStr + stat

            self.window.drawChar('████████████████',
                                 (bX - 1) * 7 + 2, self.window.piceH + bY, 'black', fontSize=textlen)
            self.window.drawChar(textStr, (bX - 1) * 7 + 2, self.window.piceH + bY, 'white', fontSize=textlen)