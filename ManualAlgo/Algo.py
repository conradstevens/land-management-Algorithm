"""
Algorithm a planter can use to plant
"""
from Planter.Planter import Planter
from Pice.Pice import Pice

class Algo:
    planter = Planter(-1, -1)

    def __init__(self, planter: Planter):
        self.planter = planter

    def turn(self) -> list:
        """
        A turn the planter will make
        :rtype: object
        :return: list
        """
        if self.planter.bagCount > self.planter.bagSize/2 + 1:
            return self.plantRight_CounterClock()

        elif self.planter.bagCount > 0:
            return self.plantRight_Clock()

    def plantRight_CounterClock(self):
        """
        Planting away from the cash
        :return: List
        """
        if self.planter.pice.piceMatrix[self.planter.y][self.planter.x + 1].isPlantable is True:  # ->
            return [1, 0]
        elif self.planter.pice.piceMatrix[self.planter.y - 1][self.planter.x].isPlantable is True:  # ^
            return [0, 1]
        elif self.planter.pice.piceMatrix[self.planter.y][self.planter.x - 1].isPlantable is True:  # <-
            return [-1, 0]
        elif self.planter.pice.piceMatrix[self.planter.y - 1][self.planter.x].isPlantable is True:  # v
            return [0, -1]
        else:
            print('TRAPED')
            return self.plantRight_Clock()

    def plantRight_Clock(self):
        """
        planting towards the cash
        :return: List
        """
        if self.planter.pice.piceMatrix[self.planter.y][self.planter.x + 1].isPlantable is True:  # ->
            return [1, 0]
        elif self.planter.pice.piceMatrix[self.planter.y + 1][self.planter.x].isPlantable is True:  # V
            return [0, -1]
        elif self.planter.pice.piceMatrix[self.planter.y - 1][self.planter.x].isPlantable is True:  # <-
            return [1, 0]
        elif self.planter.pice.piceMatrix[self.planter.y][self.planter.x - 1].isPlantable is True:  # ^
            return [-1, 0]
        else:
            print('TRAPED')
            return self.plantRight_Clock()