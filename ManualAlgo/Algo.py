"""
Algorithm a planter can use to plant
"""
from PlanterClasses.PlanterMain import Planter
from PiceClasses.Pice import Pice

class Algo:
    def __init__(self, planter: Planter):
        self.planter = planter

    def turn(self) -> list:
        """
        A turn the planter will make
        :rtype: object
        :return: Coordinates of where to move
        """
        if self.planter.bagCount > self.planter.bagSize/2 + 1:
            return self.plantRight_CounterClock()

        elif self.planter.bagCount > 0:
            return self.plantUp_Clock()

    def plantRight_CounterClock(self):
        """
        Planting away from the cash
        :return: Coordinates of where to move
        """
        if self.planter.checkVision(1, 0).isPlantable is True:  # ->
            return [1, 0]
        elif self.planter.checkVision(0, -1).isPlantable is True:  # ^
            return [0, -1]
        elif self.planter.checkVision(-1, 0).isPlantable is True:  # <-
            return [-1, 0]
        elif self.planter.checkVision(0, 1).isPlantable is True:  # v
            return [0, 1]
        else:
            print('TRAPED')
            return self.deadWalkToLand()

    def plantUp_Clock(self):
        """
        planting towards the cash
        :return: Coordinates of where to move
        """
        if self.planter.checkVision(-1, 0).isPlantable is True:  # <-
            return [-1, 0]
        elif self.planter.checkVision(0, -1).isPlantable is True:  # ^
            return [0, -1]
        elif self.planter.checkVision(1, 0).isPlantable is True:  # ->
            return [1, 0]
        elif self.planter.checkVision(0, 1).isPlantable is True:  # V
            return [0, 1]
        else:
            print('TRAPED')
            return self.deadWalk()

    def deadWalk(self):
        """
        Dead walk back to cash
        :return: Coordinates of where to move
        """
        cashCoor = self.planter.pice.findChar('C')

        if self.planter.x > cashCoor[0]:
            return [0, -1]
        elif self.planter.x < cashCoor[0]:
            return [0, 1]
        elif self.planter.y > cashCoor[1]:
            return [0, -1]
        elif self.planter.y < cashCoor[1]:
            return [0, 1]

    def deadWalkToLand(self):
        """
        Dead Walk towards planatble area
        :return: Coordinates of where to move
        """
        return [0, -1]

