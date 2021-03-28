"""
Scripts that get all the relevant information from a pice
"""

from PiceClasses.Pice import *


def getEmptyTiles(p: Pice):
    """
    Returns the number of unplanted tiles in a pice
    :rtype int
    """
    emptyCount = 0
    for r in p.piceMatrix:
        for t in r:
            if not t.isPlanted:
                emptyCount += 1