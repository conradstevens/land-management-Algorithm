import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import os
from AI.replayMemory import ReplayMemory


class PlantModel(nn.Module):
    """
    The main AI model
    at this time it is only a 2 layer network
    """
    def __init__(self, inputSize: int, hiddenSize: int, outputSize: int, lr: float):
        """
        :param inputSize: bag size, bag count, vision list
        :param hiddenSize: middle network
        :param outputSize: always 4 for now
        """
        super().__init__()
        self.inputSize, self.hiddenSize, self.outputSize = inputSize, hiddenSize, outputSize

        self.net = torch.nn.Sequential(
            nn.Linear(inputSize, hiddenSize),
            nn.ReLU(),
            nn.Linear(hiddenSize, outputSize),
            nn.ReLU()
        )
        self.opt = optim.Adam(self.net.parameters(), lr)

    def forward(self, x):
        """
        Not entirly sure... Seems to be a if statement function
        :param x:
        :return:
        """
        return self.net(x)

    def save(self, file_name='model.pth'):
        """
        Saves the model as AI/model/modelNum
        """
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class Qtrainer:
    def __init__(self, lr: float, gamma: float, batchSize):
        self.lr, self.gama, self.batchSize = lr, gamma, batchSize

    def trainStep(self, model: PlantModel, replayMemory: ReplayMemory):
        """ Trains the AI Model based on a sample of memories memeories """
        tgtModel = PlantModel(model.inputSize, model.hiddenSize, model.outputSize, self.lr)
        tgtModel.load_state_dict(model.state_dict())

        transitionSample = self._sample(model, replayMemory)
        batch = replayMemory.transitions(*zip(*transitionSample))

        stateBatch = torch.stack([s for s in batch.state])
        actionBatch = torch.stack([torch.tensor([a.max()]) for a in batch.action])
        nextStateBatch = torch.stack([ns for ns in batch.nextState])
        rewardBatch = torch.stack([r for r in batch.reward])
        doneMask = torch.stack([torch.tensor([0]) if s else torch.tensor([1]) for s in batch.done])

        with torch.no_grad():
            qValsNext = tgtModel(nextStateBatch)
            qValsNext = torch.stack([torch.tensor([a.max()]) for a in batch.action])

        actionOneHot = torch.stack([torch.tensor([torch.argmax(a).item()]) for a in batch.action])
        actionOneHot = F.one_hot(actionOneHot, 4)

        model.opt.zero_grad()
        loss = ((doneMask * (rewardBatch + qValsNext - actionBatch)) * actionOneHot).mean()
        loss.requres_grad = True
        loss.backward()
        model.opt.step()


    def _sample(self, model, replayMemory: ReplayMemory):
        if len(replayMemory) < self.batchSize:
            return replayMemory.sample(len(replayMemory))
        return replayMemory.sample(self.batchSize)

