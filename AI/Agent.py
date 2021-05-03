from PlanterClasses.PlanterMain import Planter
from PiceClasses.Pice import Pice
from PiceClasses.Pice import PiceWind
from AI.PiceScorer import PiceScore
import time


class Agent:
    """ Gets Planter information and creates AI tensors to be processed """

    def __init__(self, fileName, bagSize, viwDistance):
        # Pice Logistics
        self.fileName, self.bagSize, self.viewDistance = fileName, bagSize, viwDistance
        self.planter = Planter(bagSize=self.bagSize, viwDistance=self.viewDistance, pice=Pice(self.fileName))

        # Ai Mechanics
        self.state = self.getState()
        self.inputSize = len(self.state)
        self.piceScore = PiceScore(self.planter)

    def getState(self):
        """ :return: The input tensor """
        return tuple(self.getVisionData())

    def getVisionData(self):
        """
        Gets what is in the planters vision by:
            Tile -> [is Plantable, is Walkable]
        """
        visionData = []
        for v in self.planter.vision.visionCircle:
            nx, ny = v[0], v[1]
            if not (nx == 0 and ny == 0):
                tile = self.planter.getTile(nx=nx, ny=ny, selfRelative=True)
                visionData.append((not tile is None) and tile.isPlantable)
        return visionData

    def playAction(self, moveN, updateView=True):
        """ Trains self.model one generation
        TODO/ Teach planter to even plant
        :moveN = 1,2,3,4
        :return state after move, reward"""
        nx, ny = self._getMoveFromLst(moveN)
        self.planter.move(nx, ny, plant=True, updateView=updateView)
        return self.getState(), self.piceScore.scorePice()

    def undoAction(self, move, revTile):
        """ Undoes move spescifief """
        revMove = self._getNegMove(move)
        nx, ny = self._getMoveFromLst(revMove)
        self.planter.move(nx, ny, plant=True, revTile=revTile, updateView=False)

    def newPice(self, epoch, render=False):
        """ Creates a new pice and places the planter in it"""
        if render:
            pice = PiceWind(self.fileName, 12)
        else:
            pice = Pice(self.fileName)
        self.planter = Planter(self.bagSize, self.viewDistance, pice)
        self.piceScore.resetNewPice(epoch, self.planter)
        self.piceScore.gameNum += 1

    def playQ(self, playQ: list):
        """
        a Q of moves for the AI to play. After the Q is played the score is returned and the pice is reset
        :returns reward of path
        """
        tileSaves = []
        self.piceScore.saveScore()
        for move in playQ:
            time.sleep(0.5)
            self.playAction(move, updateView=False)
            tileSaves.append(self.planter.tileSave)

        pathReward = self.piceScore.piceScore - self.piceScore.scoreSave['piceScore']
        playQ.reverse()
        tileSaves.reverse()

        i = 0
        for move in playQ:
            time.sleep(0.5)
            self.undoAction(move, revTile=tileSaves[i])
            i += 1

        self.piceScore.loadScore()
        return pathReward

    def _getNegMove(self, move):
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



