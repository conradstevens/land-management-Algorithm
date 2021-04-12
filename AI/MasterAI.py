from AI.Agent import Agent
from AI.QTrainer import QTrainer
import torch
import random
import time


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    TODO/ To be trained?
    TODO/ Refactor to run different models
    """

    def __init__(self, agent: Agent, qTrainer: QTrainer, nEpochs: int, showEvery: int):
        # Logistical Classes
        self.agent = agent
        self.qTrainer = qTrainer
        # training loop info
        self.nEpochs = nEpochs
        self.showEvery = showEvery

    def train(self):
        """ The loop that trains the AI """
        for epoch in range(0, self.nEpochs):
            doRender = epoch % self.showEvery == 0
            print(epoch, doRender)

            self.agent.newPice(epoch, render=doRender)  # create a new pice, every showEvery
            self.playPice(doRender)

    def playPice(self, doRender):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished:
            curState = self.agent.state
            action = self.qTrainer.getAction(curState, self.doRandomMove())

            newState, reward = self.agent.playAction(action)

            self.qTrainer.learn(curState, newState, reward)

            if doRender:
                time.sleep(0.2)
        self.agent.planter.pice.terminate()

    def doRandomMove(self):
        """ :return Bool"""
        return max(0.03, (10_000 - self.agent.piceScore.gameNum) / 50_000) < random.random()


if __name__ == '__main__':
    agent = Agent(fileName='C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt',
                  bagSize=400,
                  viwDistance=2)
    qTrainer = QTrainer(gama=0.9,
                        lr=0.1,
                        epsilon=0.5,
                        maxMemory=100_000)
    masterAi = MasterAI(agent=agent,
                        qTrainer=qTrainer,
                        nEpochs=100_000,
                        showEvery=500)
    masterAi.train()
