import torch
import random
from World.planterMain import Planter
from World.pice import Pice
from World.pice import PiceWind
from AI.plantModel import PlantModel
from AI.piceScorer import PiceScore


class Agent:
    """ Gets Planter information and creates AI tensors to be processed """

    def __init__(self, fileName, bagSize, viwDistance):
        # Pice Logistics
        self.fileName, self.bagSize, self.viewDistance = fileName, bagSize, viwDistance
        self.planter = Planter(bagSize=self.bagSize, viwDistance=self.viewDistance, pice=Pice(self.fileName))

        # Ai Mechanics
        self.inputTensor = self.getInputTensor()
        self.inputSize = len(self.inputTensor)
        self.piceScore = PiceScore(self.planter)

    def getInputTensor(self):
        """ :return: The input tensor """
        return torch.FloatTensor(self.getVisionData())

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

    def playAction(self, model: PlantModel, chanceDoRand: float):
        """ Trains self.model one generation """
        self.chanceDoRand = chanceDoRand
        self.model = model
        move = self.getMove()
        nx, ny = self._getMoveFromLst(move)
        self.planter.move(nx, ny, plant=True)
        return torch.tensor(move, dtype=torch.float)

    def getMove(self):
        """ :return: returns the move for the planter to make """
        move = [0, 0, 0, 0]
        if self._doRand():
            move[random.randint(0, 3)] = 1
        else:
            prediction = self.model(self.inputTensor)
            dirNum = torch.argmax(prediction).item()
            move[dirNum] = 1
        return move

    def newPice(self, epoch, render=False):
        """ Creates a new pice and places the planter in it"""
        if render:
            pice = PiceWind(self.fileName, 12)
        else:
            pice = Pice(self.fileName)
        self.planter = Planter(self.bagSize, self.viewDistance, pice)
        self.piceScore.resetNewPice(epoch, self.planter)

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



