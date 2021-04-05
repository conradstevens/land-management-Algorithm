import torch
import numpy
import random
from PlanterClasses.PlanterMain import Planter
from PiceClasses.Pice import Pice
from AI.PlantModel import PlantModel
from tests.Tester import getBasic_Pice_and_Planter



class Agent:
    """
    Gets Planter information and creates AI tensors to be processed
    """

    def __init__(self, planter):
        self.planter = planter
        self.inputTensor = self.getInputTensor()
        self.inputSize = len(self.inputTensor)

    def getInputTensor(self):
        """
        :return: The input tensor
        """
        tList = [self.planter.bagSize, self.planter.bagCount]
        tList = tList + self.getVisionData()
        return torch.FloatTensor(tList)

    def getVisionData(self):
        """
        Gets what is in the planters vision by:
            Tile -> [is Plantable, is Walkable]
        """
        visionData = []
        for v in self.planter.vision.visionCircle:
            nx, ny = v[0], v[1]
            tile = self.planter.getTile(nx=nx, ny=ny, selfRelative=True)
            visionData.append((not tile is None) and tile.isPlantable)
            visionData.append((not tile is None) and tile.isWalkable)
        return visionData


class PiceRunner:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.chanceDoRand = 0
        self.model = None

    def playPice(self, model: PlantModel, chanceDoRand: float):
        """
        Trains self.model one generation
        """
        self.chanceDoRand = chanceDoRand
        self.model = model
        move = self.getMove()
        nx, ny = self._getMoveFromLst(move)
        self.agent.planter.move(nx, ny, plant=True)
        return torch.tensor(move, dtype=torch.float)

    def getMove(self):
        """
        :return: returns the move for the planter to make
        """
        move = [0, 0, 0, 0]
        if self._doRand():
            move[random.randint(0, 3)] = 1
        else:
            prediction = self.model(self.agent.inputTensor)
            dirNum = torch.argmax(prediction).item()
            move[dirNum] = 1
        return move

    def _doRand(self):
        return random.random() < self.chanceDoRand

    @staticmethod
    def _getMoveFromLst(move):
        if move == [0, 0, 0, 0]:
            return 0, 0
        if move == [1, 0, 0, 0]:
            return 1, 0
        if move == [0, 1, 0, 0]:
            return 0, -1
        if move == [0, 0, 1, 0]:
            return -1, 0
        else:  # move == [0, 0, 0, 1]:
            return 0, -1



