import time as tm
"""
land-management-Algorithm
Has application to large scale land management, particularly forestry and agriculture.

This program is in writen in python. Given any shaped map of plantable and unplantable land, a character will move about
the land covering every plantable point and missing every unplantable point while using as few steps as possoble.
Additionaly fuel can be added so the character can only take a finite number of steps before having to return to it's
start location for fule.

Here is a link to a video titled “Land Management Algorithm” of the algorithm in action:
https://www.youtube.com/watch?v=vGFUHFJXjKI b

Jonathan scooter Clark, an leading member of the reforestiation community has spoken with me about mentioning the
algorithm in the next version of his book: 'Step by Step, a guide to tree planting for beginners'.
"""

from PiceClasses.Pice import *
from PlanterClasses.PlanterMain import Planter
from ManualAlgo.Algo import Algo


def runManualAlgo(fileName: str, bagSize: int, viewDistance: int, stepTime: float):
    """
    Runs the planter Algorithm.
    This is a pretty lazzy algorithm that barley works. It is mostly for testing.
    """
    # Upload Pice
    pice = PiceWind(fileName, 20)   # Comment for no window run
    # pice.drawPice()                 # Comment for no window run
    # pice = Pice(fileName)         # Comment for WINDOW run

    # Set PlanterClasses Parameters
    planter = Planter(bagSize=bagSize, viwDistance=viewDistance, pice=pice)
    algo = Algo(planter)

    # Planting Loop
    while planter.finished is False:
        move = algo.turn()
        planter.move(move[0], move[1], True)
        tm.sleep(stepTime)

def runSampleManualAlgo():
    """
    A Sample test of the algorithm
    :return:
    """
    fileName = 'C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt'
    bagSize = 400
    viewDistance = 4
    stepTime = 0.5

    runManualAlgo(fileName, bagSize, viewDistance, stepTime)


def runAI():
    """
    Runs the AI ***** More Detail Later
    :return:
    """
    fileName = 'C:/Users/conra/Documents/land-management-Algorithm/Pice/Pices/Pice1.txt'
    bagSize = 400
    viewDistance = 4

if __name__ == '__main__':
    runSampleManualAlgo()




