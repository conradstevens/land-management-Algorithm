import torch
from Pice.Pice import Pice
from Pice.Window import Windw
from Planter.Planter import Planter

class AiMain():
    def __init__(self,fileNamem: str, bagSize: int, viewDistance: int):
        self.planter = Planter(bagSize, viewDistance)

    def main(self):
        """
        Runs the AI
        :return:
        """
        pass

    def getImput(self):
        """
        Gets the vector for making the decision
        :rtype torch.tensor
        """


if __name__ == '__main__':
    x = torch.tensor([5, 3])
    y = torch.tensor([2, 1])

    print(x * y)
