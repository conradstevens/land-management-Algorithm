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
        pice, planter = getBasic_Pice_and_Planter()


        self.assertAlmostEqual()


if __name__ == '__main__':
    print('*****TESTS*****')
    getBasic_Pice_and_Planter()
