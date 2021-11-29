from AI.agent import Agent
from AI.plantModel import *
from AI.plantModel import *
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

    def __init__(self, agent: Agent, trainer, trainingPices: list, hiddenSize1: int, lr: float, epsilon: float, nEpochs: int,
                 replayMemory: ReplayMemory, showEvery: int, printEvery: int, renderSleep: float, modelName: str, model=None):

        # Logistical Classes
        self.agent = agent

        # Trainer
        if model is not None:
            self.model = model
        else:
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
        self.maxScore = 0
        self.lossCount = []
        self.epochScoreCount = 0
        self.genDeadCount = 0

        # Save info
        self.hiddenSize1 = hiddenSize1
        self.modelName = (modelName + '_Is_' + str(self.agent.inputSize) + '_Hs_' + str(self.hiddenSize1))

    def runAi(self):
        """ runs the AI, track progress and saves the model"""
        self.trainLoop()
        self.saveModel()
        self.plotScores()

        print("***** Done *****")

    def trainLoop(self):
        """ The loop that trains the AI """
        for epoch in range(0, self.nEpochs):
            doRender = epoch % self.showEvery == 0
            doPrint = epoch % self.printEvery == 0

            if doPrint:
                print('Epoch num: ' + str(epoch) + '  Score: ' + str(self.epochScoreCount))

            self.epochScoreCount = 0
            for pice in self.trainingPices:
                # print(pice)
                self.agent.newPice(epoch, pice, doRender)  # create a new pice, every showEvery
                self.playPice(doRender)

            loss = self.trainer.trainStep(self.model, self.replayMemory, self.epochScoreCount)  # Trains Model
            self.lossCount.append(loss)
            self.scores.append(self.epochScoreCount)
            self.genDeadCount = 0
            self.replayMemory.piceScore = 0

            if self.epochScoreCount > self.maxScore:
                self.maxScore = self.epochScoreCount
                self.saveModel()
                print("Saved Model at Score: " + str(self.epochScoreCount))

            if loss == 0:
                break

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

        self.epochScoreCount += self.agent.piceScore.piceScore
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

    def plotScores(self):
        """ Plots the Scores once training is complete """
        plt.plot(self.scores)
        plt.xlabel('Epoch Number')
        plt.ylabel('Score')
        plt.title('Training Progress Score')
        plt.show()

        plt.plot(self.lossCount)
        plt.xlabel('Epoch Number')
        plt.ylabel('Score')
        plt.title('Training Progress Loss')
        plt.show()



if __name__ == '__main__':
    ''' Current tensor: [is plantable, is walkable] across vision circle'''

    trainingPices = ['C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train0.txt'] #  ,
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train1.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train2.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train3.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train4.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train5.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train6.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train7.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train8.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train9.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train10.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train11.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train12.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train13.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train14.txt',
                     #'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train15.txt']

    planter = Planter(bagSize=400,
                      viewDistance=2,
                      pice=Pice(trainingPices[0]))

    score = DeadPlantScore(planter)

    trainer = QtrainerHybrid(batchSize=500, scoreExpectation=15)

    model = torch.load('C:/Users/conra/Documents/land-management-Algorithm/AI/Models/QtrainHybridStart_View2')

    agent = Agent(planter, score)
    masterAi = MasterAI(agent=agent,
                        trainer=trainer,
                        trainingPices=trainingPices,
                        hiddenSize1=32,
                        lr=0.01,
                        epsilon=0.999999999,  # Chance not to make random move
                        nEpochs=50_000,
                        replayMemory=ReplayMemory(capacity=10_000),
                        showEvery=1_000,
                        printEvery=1,
                        renderSleep=0.1,
                        modelName="QtrainHybridStart",
                        model=model)

    masterAi.runAi()

