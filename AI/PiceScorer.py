from PiceClasses.Pice import Pice
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
        self.score = 0

    def scorePice(self):
        """
        :return: score of the pice
        """
        self.score = -self.planter.deadCount

