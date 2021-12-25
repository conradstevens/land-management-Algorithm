import math as math


class Vision:
    visionCircle = []  # Filled circle

    def __init__(self, rad):
        """
        Vision of planter
        """
        self.rad = rad
        self.getVisionCircle()
        self.surroundings = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def getVisionCircle(self):
        """
        sets the vision circle around a point [0, 0]
        It can later be transposed on to any location in the pice

        Note: no mater the size of a vision circle. The variables are displayed in the same order.
        """
        for x in range(0, self.rad+1):
            ang = math.acos(x / self.rad)
            y = math.floor(math.sin(ang) * self.rad)

            for yi in range(0, y + 1):
                addToListIfNotIn(self.visionCircle, [x, yi])
                addToListIfNotIn(self.visionCircle, [-x, -yi])
                addToListIfNotIn(self.visionCircle, [-x, yi])
                addToListIfNotIn(self.visionCircle, [x, -yi])


def addToListIfNotIn(l: list, elm):
    """
    Adds element to list if not in the list already
    """
    if elm not in l:
        l.append(elm)
    return l