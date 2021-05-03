from PlanterClasses.PlanterMain import Planter
from tests.PiceManager import *
from AI.Agent import Agent
from AI.Models.QTrainer import QTrainer
from AI.MasterAI import MasterAI
import unittest


def getBasic_Pice_and_Planter():
    """ gets a basic pice with 400 trees """
    pice = Pice(fileName='C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt')
    planter = Planter(bagSize=400, viwDistance=2, pice=pice)
    return pice, planter


def getBasic_AI_Classes():
    """ gets the basic AI calsses and basic planter classes """
    agent = Agent(fileName='C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt',
                  bagSize=400,
                  viwDistance=1)
    qTrainer = QTrainer(gama=0.9,
                        lr=0.1,
                        epsilon=0.5,
                        maxMemory=100_000,
                        plantReward=10,
                        deadPenalty=-30)
    masterAi = MasterAI(agent=agent,
                        qTrainer=qTrainer,
                        nEpochs=100_000,
                        showEvery=20_000)

    return agent, masterAi


class TestPiceManager(unittest.TestCase):

    def test_getEmptyTiles(self):
        """
        Tests the number of holes in a python file
        """
        pice, planter = getBasic_Pice_and_Planter()
        # Starting on cash
        self.assertEqual(getEmptyTiles(pice), 100)
        # Up 2
        planter.move(0, -1, True)
        planter.move(0, -1, True)
        self.assertEqual(getEmptyTiles(pice), 98)
        # Right 1
        planter.move(1, 0, True)
        self.assertEqual(getEmptyTiles(pice), 97)
        # Back left cant plant
        planter.move(-1, 0, True)
        self.assertEqual(getEmptyTiles(pice), 97)

    def test_DeadwalkCount(self):
        """
        Tests the number of corners in a python file
        :return:
        """
        pice, planter = getBasic_Pice_and_Planter()
        # Starting on cash
        self.assertEqual(planter.deadCount, 0)
        planter.move(0, -1, True)
        planter.move(0, -1, True)
        self.assertEqual(planter.deadCount, 0)
        planter.move(0, 1, True)
        self.assertEqual(planter.deadCount, 0)
        planter.move(0, 1, True)
        self.assertEqual(planter.deadCount, 1)
        planter.move(0, 1, True)
        self.assertEqual(planter.deadCount, 2)

    def test_Bags(self):
        pice, planter = getBasic_Pice_and_Planter()
        # Starting on Cash
        self.assertEqual(planter.bagSize, planter.bagCount)
        # Trying and failing to plant on the cash
        planter.plant()
        self.assertEqual(planter.bagSize, planter.bagCount)
        # Successfully planting
        planter.move(0, -1, True)
        self.assertEqual(planter.bagSize - 1, planter.bagCount)
        # Failing to plant on trees
        planter.plant()
        self.assertEqual(planter.bagSize - 1, planter.bagCount)

    def test_moveQ(self):
        agent, masterAi = getBasic_AI_Classes()
        agent.newPice(1, render=True)
        agent.playQ([1, 1, 1, 1])





if __name__ == '__main__':
    pass
    # print('*****TESTS*****')
    # tester = TestPiceManager()
    # tester.test_getEmptyTiles()
    # tester.test_DeadwalkCount()
    # tester.test_Bags()
    # tester.test_moveQ()
