from AI.Agent import Agent
from AI.PlantModel import PlantModel
from AI.PlantModel import Qtrainer
from tests.Tester import getBasic_Pice_and_Planter
from AI.PiceScorer import PiceScore
import PiceClasses.Pice
from PlanterClasses.PlanterMain import Planter
from collections import deque
import torch
import time


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    TODO/ To be trained?
    TODO/ Refactor to run different models
    """

    def __init__(self, agent: Agent, gama: float, lr: float, epsilon: float, nEpochs: int,
                 maxMemory: int, showEvery: int):

        # Logistical Classes
        self.agent = agent

        # Trainer
        self.model = PlantModel(self.agent.inputSize, agent.inputSize, 4)
        self.trainer = Qtrainer(self.model, lr, gama)
        self.memory = deque(maxlen=maxMemory)

        # training loop info
        self.epsilon = epsilon
        self.nEpochs = nEpochs
        self.showEvery = showEvery

    def train(self):
        """ The loop that trains the AI """
        for epoch in range(0, self.nEpochs):
            doRender = epoch % self.showEvery == 0

            print(epoch, doRender)

            self.agent.newPice(epoch, render=doRender)  # create a new pice, every showEvery
            self.playPice()

    def playPice(self):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished:
            curState = self.agent.inputTensor
            action = self.agent.playAction(model=self.model, chanceDoRand=self.chanceofRandMove())
            reward = torch.tensor(self.agent.piceScore.scorePice(), dtype=torch.float)
            nextState = self.agent.getInputTensor()
            self._remember(curState, action, reward, nextState, agent.planter.finished)

            time.sleep(1)
        self.agent.planter.pice.terminate()


    # def playPiceX(self):
    #     """
    #     runs through the pice with the current model
    #     TODO
    #     """
    #     self.stats.drawStats()
    #     while not agent.planter.finished:
    #         curState = self.agent.inputTensor
    #         action = self.piceRunner.playAction(self.model, self.chanceofRandMove())  # make move and get move as tensor
    #         reward = torch.tensor(self.agent.piceScore.scorePice(), dtype=torch.float)
    #         nextState = self.agent.getInputTensor()
#
    #         self._remember(curState, action, reward, nextState, planter.finished)
    #         print((curState, action, reward, nextState, planter.finished))
#
    #         time.sleep(0.1)
    #         return

    def _remember(self, state, move, reward, nextState, done):
        """
        Records each move and associated reward
        """
        self.memory.append((state, move, reward, nextState, done))

    def chanceofRandMove(self):
        return (80 - self.agent.piceScore.gameNum) / 200

if __name__ == '__main__':
    agent = Agent(fileName='C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt',
                  bagSize=400,
                  viwDistance=1)
    masterAi = MasterAI(agent=agent,
                        gama=0.9,
                        lr=0.1,
                        epsilon=0.5,
                        nEpochs=11,
                        maxMemory=100_000,
                        showEvery=5)
    masterAi.train()
