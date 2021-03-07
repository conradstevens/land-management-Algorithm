import math as math

class Vision():

    rad = -1
    rawCircle = []
    visionCircle = []

    def __init__(self, rad):
        """
        Vision of planter
        """
        self.rad = rad
        self.getVisionCircle()

    def getVisionCircle(self):
        """
        sets the vision circle around a point [0, 0]
        It can later be transposed on to any location in the pice
        """
        circum = []
        for x in range(0, self.rad+1):
            ang = math.acos(x/self.rad)
            y = round(math.sin(ang)*self.rad)

            circum = addToListIfNotIn(circum, [x, y])
            circum = addToListIfNotIn(circum, [-x, -y])
            circum = addToListIfNotIn(circum, [-x, y])
            circum = addToListIfNotIn(circum, [x, -y])

        self.visionCircle = circum
        print(circum)


def addToListIfNotIn(l: list, elm):
    """
    Adds element to list if not in the list already
    """
    if elm not in l:
        l.append(elm)
    return l


















    #def getVisionCircle(self):
    #    """
    #    sets the vision circle around a point [0, 0]
    #    It can later be transposed on to any location in the pice
    #    """
    #    candidateCircle = self.getCandidateVission()
#
    #    print(candidateCircle)
    #    print(self.rawCircle)
#
    #    for iCand in range(0, len(candidateCircle)):
    #        cand = candidateCircle[iCand]
    #        raw = self.rawCircle[iCand]
#
    #        ceilDist = abs(self.getDistance(cand, raw))
#
    #        if ceilDist < 2**0.5/2:
    #            self.visionCircle.append(cand)
#
    #def getCandidateVission(self):
    #    """
    #    Returns as list of candidates that could be in the vision circle.
    #    Note -  Candidate circle >= vision circle
    #    :return: List
    #    """
    #    candidateCirc = []
    #    iterCount = math.ceil(2 * math.pi * self.rad)*4
    #    iterRadians = 2 * math.pi / iterCount
#
    #    for iter in range(1, iterCount):
    #        # raw values used do determin incluseion
    #        self.rawCircle.append([self.rad*math.cos(iter * iterRadians), self.rad*math.sin(iter * iterRadians)])
#
    #        # max radius values
    #        candTile = [self.ceilingCoor(self.rad*math.cos(iter * iterRadians)),
    #                    self.ceilingCoor(self.rad*math.sin(iter * iterRadians))]
#
    #        if candTile not in candidateCirc:
    #            candidateCirc.append(candTile)
    #        else:
    #            self.rawCircle.pop()
#
    #    return candidateCirc
#
    #def getDistance(self, p1: list, p2: list):
    #    """
    #    Returns the distance between p1 and p2
    #    """
    #    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
#
    #def ceilingCoor(self, coorVal):
       #"""
       #Returns the ceiling value of the coordinate by maximizing the distance from orrigin
       #"""
       #if coorVal > 0:
       #    return math.ceil(coorVal)
       #else:
       #    return math.floor(coorVal)

