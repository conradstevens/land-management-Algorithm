from AI.agent import Agent
from AI.plantModel import *
from AI.plantModel import *
from AI.replayMemory import ReplayMemory
from AI.piceScorer import *
from World.planterMain import Planter
from World.pice import Pice
# import matplotlib.pyplot as plt
import torch
import time

import numpy as np


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    TODO/ To be trained?
    TODO/ Refactor to run different models
    """

    def __init__(self, agent: Agent, trainer, trainingPices: list, hiddenSize1: int, lr: float, epsilon: float, nEpochs: int,
                 replayMemory: ReplayMemory, showEvery: int, printEvery: int, renderSleep: float, modelName: str):

        # Logistical Classes
        self.agent = agent

        # Trainer
        self.model = PlantModel(self.agent.inputSize, hiddenSize1, 4, lr)
        self.trainer = trainer
        self.replayMemory = replayMemory
        self.trainingPices = trainingPices

        # Training loop info
        self.epsilon = epsilon
        self.nEpochs = nEpochs
        self.showEvery = showEvery
        self.printEvery = printEvery
        self.renderSleep = renderSleep

        # Progress Tracker
        self.scores = []
        self.setScoreCount = 0
        self.genDeadCount = 0

        # Save info
        self.hiddenSize1 = hiddenSize1
        self.modelName = (modelName + '_Is_' + str(self.agent.inputSize) + '_Hs_' + str(self.hiddenSize1))

    def runAi(self):
        """ runs the AI, track progress and saves the model"""
        self.trainLoop()
        self.saveModel()

        print("pass")

    def trainLoop(self):
        """ The loop that trains the AI """
        for epoch in range(0, self.nEpochs):
            doRender = epoch % self.showEvery == 0
            doPrint = epoch % self.printEvery == 0

            if doPrint:
                print('Epoch num: ' + str(epoch))

            for pice in self.trainingPices:
                # print(pice)
                self.agent.newPice(epoch, pice, doRender)  # create a new pice, every showEvery
                self.playPice(doRender)

            self.scores.append(self.setScoreCount)
            self.trainer.trainStep(self.model, self.replayMemory, self.genDeadCount)
            self.setScoreCount = 0
            self.genDeadCount = 0
            self.replayMemory.piceScore = 0

    def playPice(self, doRender):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished and agent.piceScore.downStreak < 10:
            curState = self.agent.inputTensor
            surround = self.agent.getSurroundingTensor()
            action = self.agent.playAction(model=self.model, chanceDoRand=self.chanceofRandMove())
            reward = torch.tensor([self.agent.piceScore.scoreMove()], dtype=torch.float)
            nextState = self.agent.getInputTensor()
            move = torch.tensor([action.argmax().item()])

            self.replayMemory.moveDataPush(curState, surround, action, nextState, reward, move, agent.planter.finished)
            if doRender:
                time.sleep(self.renderSleep)

        self.setScoreCount += self.agent.piceScore.piceScore
        self.genDeadCount += self.agent.piceScore.deadCount
        self.replayMemory.piceScore += self.agent.piceScore.piceScore
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

    trainingPices = ['C:/Users/conra/Documents/land-management-Algorithm/World/Pices/smallTrain3/Train7.txt']

    planter = Planter(bagSize=400,
                      viewDistance=1,
                      pice=Pice(trainingPices[0]))

    score = DeadPlantScore(planter)

    trainer = PiceTrainer(batchSize=500)

    agent = Agent(planter, score)
    masterAi = MasterAI(agent=agent,
                        trainer=trainer,
                        trainingPices=trainingPices,
                        hiddenSize1=32,
                        lr=0.01,
                        epsilon=0.9999999999999,  # Chance not to make random move
                        nEpochs=2000,
                        replayMemory=ReplayMemory(capacity=100_000),
                        showEvery=200,
                        printEvery=100,
                        renderSleep=0.000,
                        modelName="Model1")

    masterAi.runAi()

