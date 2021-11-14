from AI.agent import Agent
from AI.plantModel import PlantModel
from AI.plantModel import Qtrainer
from AI.replayMemory import ReplayMemory
from AI.piceScorer import *
from World.planterMain import Planter
from World.pice import Pice
import matplotlib.pyplot as plt
import torch
import time


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    TODO/ To be trained?
    TODO/ Refactor to run different models
    """

    def __init__(self, agent: Agent, trainingPices: list, hiddenSize1: int, gama: float, lr: float, epsilon: float, nEpochs: int,
                 batchSize: int, replayMemory: ReplayMemory, showEvery: int, printEvery: int, renderSleep: float,
                 modelName: str):

        # Logistical Classes
        self.agent = agent

        # Trainer
        self.model = PlantModel(self.agent.inputSize, hiddenSize1, 4, lr)
        self.trainer = Qtrainer(lr, gama, batchSize)
        self.replayMemory = replayMemory
        self.trainingPices = trainingPices

        # Training loop info
        self.epsilon = epsilon
        self.nEpochs = nEpochs
        self.batchSize = batchSize
        self.showEvery = showEvery
        self.printEvery = printEvery
        self.renderSleep = renderSleep

        # Progress Tracker
        self.scores = []
        self.setScoreCount = 0

        # Save info
        self.hiddenSize1 = hiddenSize1
        self.modelName = (modelName + '_Is_' + str(self.agent.inputSize) + '_Hs_' + str(self.hiddenSize1))

    def runAi(self):
        """ runs the AI, track progress and saves the model"""
        self.trainLoop()
        self.saveModel()
        plt.plot(self.scores)
        plt.show()
        print("pass")

    def trainLoop(self):
        """ The loop that trains the AI """
        for epoch in range(0, self.nEpochs):
            doRender = epoch % self.showEvery == 0
            doPrint = epoch % self.printEvery == 0

            if doPrint:
                print('Epoch num: ' + str(epoch))

            for pice in self.trainingPices:
                self.agent.newPice(epoch, pice, doRender)  # create a new pice, every showEvery
                self.playPice(doRender)

            self.scores.append(self.setScoreCount)
            self.setScoreCount = 0
            self.trainer.trainStep(self.model, self.replayMemory)

    def playPice(self, doRender):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished and agent.piceScore.downStreak < 10:
            curState = self.agent.inputTensor
            surround = self.agent.getSurroundingTensor()
            action = self.agent.playAction(model=self.model, chanceDoRand=self.chanceofRandMove())
            reward = torch.tensor([self.agent.piceScore.scoreMove()], dtype=torch.float)
            nextState = self.agent.getInputTensor()
            move = torch.tensor([action.argmax().item()])

            self.replayMemory.push(curState, surround, action, nextState, reward, move, agent.planter.finished)
            if doRender:
                time.sleep(self.renderSleep)

        self.setScoreCount += self.agent.piceScore.piceScore
        self.agent.planter.pice.terminate()

    def chanceofRandMove(self):
        """ Chance of doing a random move """
        return 1 - (self.epsilon + self.agent.piceScore.gameNum * (1 - self.epsilon) / self.nEpochs)

    def saveModel(self):
        """ Saves the model """
        if self.modelName is not None:
            torch.save(self.model,
                       "C:/Users/conra/Documents/land-management-Algorithm/AI/Models/" + self.modelName)


if __name__ == '__main__':
    ''' Current tensor: [is plantable, is walkable] across vision circle'''

    trainingPices = ['C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train1.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train2.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train3.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train4.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train5.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train6.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train7.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train8.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train9.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train10.txt']

    planter = Planter(bagSize=400,
                      viewDistance=1,
                      pice=Pice(trainingPices[0]))

    score = DeadPlantScore(planter)

    agent = Agent(planter, score)
    masterAi = MasterAI(agent=agent,
                        trainingPices=trainingPices,
                        hiddenSize1=32,
                        gama=0.9,
                        lr=0.01,
                        epsilon=0.9999999999999,  # Chance not to make random move
                        nEpochs=10000,
                        batchSize=500,
                        replayMemory=ReplayMemory(capacity=100_000),
                        showEvery=200,
                        printEvery=100,
                        renderSleep=0.000,
                        modelName="Model1")

    masterAi.runAi()

