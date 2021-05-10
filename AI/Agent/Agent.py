from PlanterClasses.PlanterMain import Planter
from PiceClasses.Pice import Pice
from PiceClasses.Pice import PiceWind
from AI.PiceScorer import PiceScore
from AI.Agent.Action import Action
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

        # Helper Classes
        self.action = Action(self.planter, self.piceScore)

    def getState(self):
        """ :return: The input tensor """
        return tuple(self.getVisionData())

    def newPice(self, epoch, render=False):
        """ Creates a new pice and places the planter in it"""
        if render:
            pice = PiceWind(self.fileName, 12)
        else:
            pice = Pice(self.fileName)
        self.planter = Planter(self.bagSize, self.viewDistance, pice)
        self.action.planter = self.planter
        self.piceScore.resetNewPice(epoch, self.planter)
        self.piceScore.gameNum += 1

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
        self.action.playAction(moveN, updateView=True)
        return self.getState(), self.piceScore.scorePice()

