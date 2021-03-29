from PiceClasses.Pice import *
from PlanterClasses.PlanterMain import Planter
from AI.PiceManager import *
import unittest


def getBasic_Pice_and_Planter():
    """
    gets a basic pice with 400 trees
    :rtype Pice
    """
    pice = Pice(fileName='C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt')
    planter = Planter(bagSize=400, viwDistance=1, pice=pice)
    pice.placePlaner(planter)
    return pice, planter


class TestPiceManager(unittest.TestCase):

    def test_getEmptyTiles(self):
        """
        Tests the number of holes in a python file
        """
        pice, planter = getBasic_Pice_and_Planter()
        # Starting on cash
        self.assertEqual(getEmptyTiles(pice), 100)
        # Up 2
        planter.move(0, -1)
        planter.plant()
        planter.move(0, -1)
        planter.plant()
        self.assertEqual(getEmptyTiles(pice), 98)
        # Right 1
        planter.move(1, 0)
        planter.plant()
        self.assertEqual(getEmptyTiles(pice), 97)
        # Back left cant plant
        planter.move(-1, 0)
        planter.plant()
        self.assertEqual(getEmptyTiles(pice), 96)

    def test_DeadwalkCount(self):
        """
        Tests the number of corners in a python file
        :return:
        """
        pice, planter = getBasic_Pice_and_Planter
        # Starting on cash





if __name__ == '__main__':
    print('*****TESTS*****')
    tester = TestPiceManager()
    tester.test_getEmptyTiles()
