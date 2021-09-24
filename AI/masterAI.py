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

    def __init__(self, agent: Agent, gama: float, lr: float, epsilon: float, nEpochs: int, batchSize: int,
                 replayMemory: ReplayMemory, showEvery: int, printEvery: int, renderSleep: float):

        # Logistical Classes
        self.agent = agent

        # Trainer
        self.model = PlantModel(self.agent.inputSize, 32, 4, lr)
        self.trainer = Qtrainer(lr, gama, batchSize)
        self.replayMemory = replayMemory

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

            self.agent.newPice(epoch, render=doRender)  # create a new pice, every showEvery
            self.playPice(doRender)

    def playPice(self, doRender):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished:
            # self.model.net.zero_grad()
            curState = self.agent.inputTensor
            action = self.agent.playAction(model=self.model, chanceDoRand=self.chanceofRandMove())
            reward = torch.tensor([self.agent.piceScore.scorePice()])
            nextState = self.agent.getInputTensor()

            self.replayMemory.push(curState, action, nextState, reward, agent.planter.finished)

            if doRender:
                time.sleep(self.renderSleep)

        self.agent.planter.pice.terminate()
        self.trainer.trainStep(self.model, replayMemory)

    def chanceofRandMove(self):
        return 1 - (self.epsilon + self.agent.piceScore.gameNum * (1 - self.epsilon) / self.nEpochs)

if __name__ == '__main__':
    ''' Current tensor: [is plantable, is walkable] across vision circle'''

    agent = Agent(fileName='C:/Users/conra/Documents/land-management-Algorithm/World/Pices/pice1.txt',
                  bagSize=400,
                  viwDistance=1)

    replayMemory = ReplayMemory(capacity=100_000)

    masterAi = MasterAI(agent=agent,
                        gama=0.9,
                        lr=0.01,
                        epsilon=0.8,
                        nEpochs=1001,
                        batchSize=100,
                        replayMemory=replayMemory,
                        showEvery=1000,
                        printEvery=100,
                        renderSleep=0.01)
    masterAi.trainLoop()
