import torch
import numpy
from PlanterClasses.PlanterMain import Planter
from PiceClasses.Pice import Pice
from tests.Tester import getBasic_Pice_and_Planter


class Agent:
    """
    Gets Planter information and creates AI tensors to be processed
    """

    def __init__(self, planter):
        self.planter = planter
        self.tList = []
        self.inputTensor = self.getAITensor()

        self.n_games = 0
        self.epsilon = 0
        self.gama = 0.9
        # self.model =

    def getAITensor(self):
        self.tList = []
        self.tList.append(self.planter.bagSize)
        self.tList.append(self.planter.bagCount)
        self.setVary()
        return torch.FloatTensor(self.tList)

    def setVary(self):
        """
        Gets what is in the planters vision by:
            Tile -> [is Plantable, is Walkable]
        """
        for v in self.planter.vision.visionCircle:
            nx, ny = v[0], v[1]
            tile = self.planter.getTile(nx=nx, ny=ny, selfRelative=True)
            self.tList.append((not tile is None) and tile.isPlantable)
            self.tList.append((not tile is None) and tile.isWalkable)

    def train(self):
        pass


if __name__ == '__main__':
    pice, planter = getBasic_Pice_and_Planter()
    agent = Agent(planter)
    agent.getAITensor()
