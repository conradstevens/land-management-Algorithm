from AI.agent import Agent
from AI.plantModel import PlantModel
from AI.plantModel import Qtrainer
from AI.replayMemory import ReplayMemory
import torch
import time


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    TODO/ To be trained?
    TODO/ Refactor to run different models
    """

    def __init__(self, agent: Agent, trainingPices: list, gama: float, lr: float, epsilon: float, nEpochs: int,
                 batchSize: int, replayMemory: ReplayMemory, showEvery: int, printEvery: int, renderSleep: float):

        # Logistical Classes
        self.agent = agent

        # Trainer
        self.model = PlantModel(self.agent.inputSize, 32, 4, lr)
        self.trainer = Qtrainer(lr, gama, batchSize)
        self.replayMemory = replayMemory
        self.trainingPices = trainingPices

        # training loop info
        self.epsilon = epsilon
        self.nEpochs = nEpochs
        self.batchSize = batchSize
        self.showEvery = showEvery
        self.printEvery = printEvery
        self.renderSleep = renderSleep

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

            self.trainer.trainStep(self.model, replayMemory)

    def playPice(self, doRender):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished and self.agent.piceScore.piceScore > -20:
            curState = self.agent.inputTensor
            surround = self.agent.getSurroundingTensor()
            action = self.agent.playAction(model=self.model, chanceDoRand=self.chanceofRandMove())
            reward = torch.tensor([self.agent.piceScore.scorePice()], dtype=torch.float)
            nextState = self.agent.getInputTensor()
            move = torch.tensor([action.argmax().item()])

            # curState.requires_grad_(True)
            # action.requires_grad_(False)
            # nextState.requires_grad_(False)
            # reward.requires_grad_(True)

            self.replayMemory.push(curState, surround, action, nextState, reward, move, agent.planter.finished)
            if doRender:
                time.sleep(self.renderSleep)

        self.agent.planter.pice.terminate()

    def chanceofRandMove(self):
        return 1 - (self.epsilon + self.agent.piceScore.gameNum * (1 - self.epsilon) / self.nEpochs)

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

    agent = Agent(fileName=trainingPices[0],  # Place holder function
                  bagSize=400,
                  viwDistance=3)

    replayMemory = ReplayMemory(capacity=100_000)

    masterAi = MasterAI(agent=agent,
                        trainingPices=trainingPices,
                        gama=0.9,
                        lr=0.01,
                        epsilon=0.9999999999,  # Chance not to make random move
                        nEpochs=100_001,
                        batchSize=100,
                        replayMemory=replayMemory,
                        showEvery=500,
                        printEvery=100,
                        renderSleep=0.005)

    masterAi.trainLoop()
