"""
Planter that moves and makes decisions in the land
"""
import Pice.Pice


class Planter:
    pice Pice
    bagSize = -1
    x, y, = -1, -1

    def __init__(self, pice: Pice, bagSize: int):
        """
        Planter
        :param pice:
        :param bagsize:
        """
        self.pice = pice
        self.bagSize = bagSize

        self.pice
