import torch
from AI.plantModel import PlantModel
from AI.agent import Agent
import time


def loadModel(modeldir: str):
    """ Loads the model """
    model = torch.load(modeldir)
    return model


def playPice(model: PlantModel, agent: Agent, pice: str):
    """ Play all the pices in the cue"""
    agent.newPice(1, pice, True)
    while not agent.planter.finished and agent.piceScore.downStreak < 10:
        agent.playAction(model=model, chanceDoRand=0)
        agent.piceScore.scorePice()
        time.sleep(0.01)
    agent.planter.pice.terminate()


if __name__ == '__main__':
    model = loadModel(modeldir='C:/Users/conra/Documents/land-management-Algorithm/AI/Models/Model1_Is_28_Hs_64')

    piceCue = ['C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train1.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train2.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train3.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train4.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train5.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train6.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train7.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train8.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train9.txt',
               'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/Train10.txt']

    agent = Agent(fileName=piceCue[0],  # Place holder function
                  bagSize=400,
                  viwDistance=3)

    for pice in piceCue:
        playPice(model, agent, pice)
