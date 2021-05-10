""" Action That a planter can take """

from PlanterClasses.PlanterMain import Planter
from AI.PiceScorer import PiceScore
import time


class Action:
    def __init__(self, planter: Planter, piceScore: PiceScore):
        self.planter = planter
        self.piceScore = piceScore

    def playAction(self, moveN):
        """ Trains self.model one generation
        TODO/ Teach planter to even plant
        :moveN = 1,2,3,4
        :return state after move, reward"""
        nx, ny = self._getMoveFromLst(moveN)
        self.planter.move(nx, ny, plant=True)

    def playQ(self, playQ: list):
        """
        a Q of moves for the AI to play. After the Q is played the score is returned and the pice is reset
        :returns reward of path
        """
        self.planter.visionOn = False
        tileSaves = []
        self.piceScore.saveScore()
        for move in playQ:
            time.sleep(0.5)
            self.playAction(move)
            tileSaves.append(self.planter.tileSave)

        pathReward = self.piceScore.piceScore - self.piceScore.scoreSave['piceScore']
        playQ.reverse()
        tileSaves.reverse()

        i = 0
        for move in playQ:
            time.sleep(0.5)
            self.undoAction(move=move, revTile=tileSaves[i])
            i += 1

        self.piceScore.loadScore()
        self.planter.visionOn = True
        return pathReward

    def undoAction(self, move, revTile):
        """ Undoes move spescifief """
        revMove = self._getNegMove(move)
        nx, ny = self._getMoveFromLst(revMove)
        self.planter.move(nx, ny, plant=True, revTile=revTile, updateView=False)

    @staticmethod
    def _getNegMove(move):
        """ retunr: x, y"""
        if move == 0:
            return 2
        if move == 1:
            return 3
        if move == 2:
            return 0
        if move == 3:
            return 1

    @staticmethod
    def _getMoveFromLst(move):
        """ retunr: x, y"""
        if move == 0:
            return 1, 0
        if move == 1:
            return 0, -1
        if move == 2:
            return -1, 0
        if move == 3:
            return 0, 1