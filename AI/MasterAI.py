from AI.Agent import Agent
from AI.Models.QTrainer import QTrainer
import random
import time


class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    """

    def __init__(self, agent: Agent, qTrainer: QTrainer, nEpochs: int, showEvery: int):
        # Logistical Classes
        self.agent = agent
        self.qTrainer = qTrainer
        self.randChance = None  # TODO move to Model
        # training loop info
        self.nEpochs = nEpochs
        self.showEvery = showEvery

    def train(self):
        """ The loop that trains the AI """
        for epoch in range(0, self.nEpochs):
            doRender = epoch % self.showEvery == 0
            if epoch % 500 == 0:
                print(f'on gen {epoch}, random explore chance at: {self.randChance} loading...')

            self.agent.newPice(epoch, render=doRender)  # create a new pice, every showEvery
            self.playPice()
            self.qTrainer.saveQToCSV(doSave=doRender)

    def playPice(self):
        """ runs through the pice and updates the Q-table"""
        while not agent.planter.finished:
            curState = self.agent.state
            action = self.qTrainer.getAction(curState, self.doRandomMove())
            newState, reward = self.agent.playAction(action)
            self.qTrainer.learn(curState, newState, reward)

        self.agent.planter.pice.terminate()

    def doRandomMove(self):
        """ :return Bool"""
        endingChance = 0.03
        startChance = 0.2
        self.randChance = max(endingChance,
                              (startChance * self.nEpochs - self.agent.piceScore.gameNum) / (self.nEpochs))
        return self.randChance < random.random()


if __name__ == '__main__':
    agent = Agent(fileName='C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt',
                  bagSize=400,
                  viwDistance=2)
    qTrainer = QTrainer(gama=0.9,
                        lr=0.1,
                        epsilon=0.5,
                        maxMemory=100_000,
                        plantReward=10,
                        deadPenalty=-30)
    masterAi = MasterAI(agent=agent,
                        qTrainer=qTrainer,
                        nEpochs=100_000,
                        showEvery=5_000)
    masterAi.train()
