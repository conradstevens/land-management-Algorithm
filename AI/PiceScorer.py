from PiceClasses.Pice import Pice
import torch
from PlanterClasses.PlanterMain import Planter


class PiceScore:
    """
    Scores the pice based on what move is best
    TODO add squarness to score
    TODO Maybe reward tree planting - Is this different form peanalizing dead walking?
    TODO reward size of bagups - would incorporate function that optimizes fule use based on weight of trees carried
    """

    def __init__(self, planter: Planter):
        self.planter, self.pice = planter, planter.pice
        self.oldScore = 0
        self.score = 0
        self.deltaScore = 0

    def scorePice(self):
        """
        :return: score of the pice
        """
        self.oldScore = self.score
        self.score = self.planter.plantCount - self.planter.deadCount
        self.deltaScore = torch.tensor(self.score - self.oldScore, dtype=torch.float)
        return self.score


