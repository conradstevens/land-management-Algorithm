import torch
from World.pice import Pice
from AI.plantModel import PlantModel
from AI.agent import Agent
from AI.piceScorer import *
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
        agent.piceScore.scoreMove()
        time.sleep(0.1)
    agent.planter.pice.terminate()


if __name__ == '__main__':
    model = loadModel(modeldir='C:/Users/conra/Documents/land-management-Algorithm/AI/Models/Qtrain1_Is_4_Hs_32')

    trainingPices = ['C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train0.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train1.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train2.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train3.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train4.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train5.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train6.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train7.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train8.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train9.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train10.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train11.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train12.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train13.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train14.txt',
                     'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train15.txt']

    planter = Planter(bagSize=400,
                      viewDistance=1,
                      pice=Pice(trainingPices[0]))

    score = DeadPlantScore(planter)

    agent = Agent(planter, score)

    for pice in trainingPices:
        playPice(model, agent, pice)
