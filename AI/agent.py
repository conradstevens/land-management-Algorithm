import torch
import random
from World.planterMain import Planter
from World.pice import Pice
from World.pice import PiceWind
from AI.plantModel import PlantModel
from AI.piceScorer import PiceScore


class Agent:
    """ Gets Planter information and creates AI tensors to be processed """

    def __init__(self, planter, piceScore):
        # Pice Logistics
        self.planter = planter
        self.piceScore = piceScore

        # Ai Mechanics
        self.inputTensor = self.getInputTensor()
        self.inputSize = len(self.inputTensor)

    def getInputTensor(self):
        """ :return: The input tensor """
        visionData = []
        for v in self.planter.vision.visionCircle:
            nx, ny = v[0], v[1]
            if (nx, ny) != (0, 0):
                tile = self.planter.getTile(nx=nx, ny=ny, selfRelative=True)
                visionData.append((not tile is None) and tile.isPlantable)
                # visionData.append((not tile is None) and tile.isWalkable)

        return torch.Tensor(visionData)

    def getSurroundingTensor(self):
        """ :return: The input tensor """
        suround = []
        for v in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            nx, ny = v[0], v[1]
            tile = self.planter.getTile(nx=nx, ny=ny, selfRelative=True)
            suround.append((not tile is None) and tile.isPlantable)

        return torch.Tensor(suround)

    def playAction(self, model: PlantModel, chanceDoRand: float):
        """ Plays the action and returns the tensor used """
        move = [0, 0, 0, 0]
        if self._doRand(chanceDoRand):
            move[random.randint(0, 3)] = 1
            prediction = torch.tensor(move, dtype=torch.float)
        else:
            prediction = model(self.inputTensor)
            dirNum = torch.argmax(prediction).item()
            move[dirNum] = 1

        nx, ny = self._getMoveFromLst(move)
        # print(str(self.planter.x + nx) + " - " + str(self.planter.y + ny))
        self.planter.move(nx, ny, plant=True)
        self.inputTensor = self.getInputTensor()

        return prediction

    def newPice(self, epoch, fileName=None, render=False):
        """ Creates a new pice and places the planter in it"""
        if render:
            pice = PiceWind(fileName, 12)
        else:
            pice = Pice(fileName)
        self.planter = Planter(self.planter.bagSize, self.planter.viewDistance, pice)
        self.piceScore.resetNewPice(epoch, self.planter)
        self.inputTensor = self.getInputTensor()

    def _doRand(self, chanceDoRand):
        return random.random() < chanceDoRand

    @staticmethod
    def _getMoveFromLst(move):
        if move == [0, 0, 0, 0]:  # No Move
            return 0, 0
        if move == [1, 0, 0, 0]:  # Right
            return 1, 0
        if move == [0, 1, 0, 0]:  # Up
            return 0, -1
        if move == [0, 0, 1, 0]:  # Left
            return -1, 0
        else:  # move == [0, 0, 0, 1]:  # Down
            return 0, 1
