from AI.Agent import Agent
from AI.Agent import PiceRunner
from AI.PlantModel import PlantModel
from AI.PlantModel import Qtrainer
from tests.Tester import getBasic_Pice_and_Planter
import PiceClasses.Pice
from PlanterClasses.PlanterMain import Planter
import random
import time


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models. TODO/ To be trained?
    """

    def __init__(self, agent: Agent, piceRunner: PiceRunner, gama: float, lr: float):
        self.agent, self.piceRunner = agent, piceRunner
        self.gama, self.lr = gama, lr
        self.curModel = PlantModel(self.agent.inputSize, agent.inputSize, 4)
        self.nGames = 0
        self.highScore = 0
        # TODO self.highScoreModel

    def playPice(self):
        """
        runs through the pice with the current model
        """
        for i in range(1, 200):
            time.sleep(0.05)
            self.piceRunner.playPice(self.curModel, self.chanceofRandMove())

    def chanceofRandMove(self):
        return (80 - self.nGames) / 200


if __name__ == '__main__':
    # pice, planter = getBasic_Pice_and_Planter()
    pice = PiceClasses.Pice.PiceWind('C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt', 12)
    planter = Planter(400, 3, pice)


    agent = Agent(planter)
    piceRunner = PiceRunner(agent)
    masterAi = MasterAI(agent, piceRunner, gama=0.9, lr=0.1)
    masterAi.playPice()