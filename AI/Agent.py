import torch
import numpy
import random
from PlanterClasses.PlanterMain import Planter
from PiceClasses.Pice import Pice
from PiceClasses.Pice import PiceWind
from AI.PiceScorer import PiceScore
from tests.Tester import getBasic_Pice_and_Planter


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

    def playAction(self, moveN):
        """ Trains self.model one generation
        :return state after move, reward"""
        nx, ny = self._getMoveFromLst(moveN)
        self.planter.move(nx, ny, plant=True)
        return self.getState(), self.piceScore.scorePice()

    def newPice(self, epoch, render=False):
        """ Creates a new pice and places the planter in it"""
        if render:
            pice = PiceWind(self.fileName, 12)
        else:
            pice = Pice(self.fileName)
        self.planter = Planter(self.bagSize, self.viewDistance, pice)
        self.piceScore.resetNewPice(epoch, self.planter)
        self.piceScore.gameNum += 1

    @staticmethod
    def _getMoveFromLst(move):
        if move == 1:
            return 1, 0
        if move == 2:
            return 0, -1
        if move == 3:
            return -1, 0
        else:  # 4
            return 0, 1



