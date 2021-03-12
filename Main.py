import time as tm
"""
land-management-Algorithm
Has application to large scale land management, particularly forestry and agriculture.

This program is in writen in python. Given any shaped map of plantable and unplantable land, a character will move about
the land covering every plantable point and missing every unplantable point while using as few steps as possoble.
Additionaly fuel can be added so the character can only take a finite number of steps before having to return to it's
start location for fule.

Here is a link to a video titled “Land Management Algorithm” of the algorithm in action:
https://www.youtube.com/watch?v=vGFUHFJXjKI

Jonathan scooter Clark, an leading member of the reforestiation community has spoken with me about mentioning the
algorithm in the next version of his book: 'Step by Step, a guide to tree planting for beginners'.
"""

from Pice.Pice import Pice
from Pice.Window import Windw
from Planter.Planter import Planter
from ManualAlgo.Algo import Algo

def runManualAlgo(windowX: int, windowY: int, fileNamem: str, bagSize: int, viewDistance: int, stepTime: float):
    """
    Runs the planter Algorithm.
    This is a pretty lazzy algorithm that barley works. It is mostly for testing.
    """
    # Upload Pice
    windw = Windw(windowX, windowY)
    pice = Pice()
    pice.loadPiceMatrix(windw, fileNamem)
    pice.drawPice()

    # Set Planter Perameters
    planter = Planter(bagSize=bagSize, viwDistance=viewDistance)
    pice.placePlaner(planter)
    algo = Algo(planter)
    tm.sleep(0.10)

    # Planting Loop
    while planter.finished is False:
        tm.sleep(stepTime)
        move = algo.turn()
        planter.move(move[0], move[1])
        planter.plant()

    tm.sleep(1)


def runSampleManualAlgo():
    """
    A Sample test of the algorithm
    :return:
    """
    windowX, windowY = 18, 21
    fileName = 'C:/Users/conra/Documents/land-management-Algorithm/Pice/Pices/Pice1.txt'
    bagSize = 400
    viewDistance = 4
    stepTime = 0.01

    runManualAlgo(windowX, windowY, fileName, bagSize, viewDistance, stepTime)


if __name__ == '__main__':
    runSampleManualAlgo()




