import torch


class PlantModel(torch.nn.Module):
    """
    The main AI model
    at this time it is only a 2 layer network
    """
    def __init__(self, inputSize: int, hiddenSize: int, outputSize: int):
        """
        :param inputSize: bag size, bag count, vision list
        :param hiddenSize: middle network
        :param outputSize: always 4 for now
        """
        super().__init__()
        self.linear1 = torch.nn.Linear(inputSize, hiddenSize)
        self.linear2 = torch.nn.Linear(hiddenSize, outputSize)

    def forward(self):
        pass

