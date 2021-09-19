import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import os
import copy
from AI.replayMemory import ReplayMemory


class PlantModel(nn.Module):
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
        self.linear1 = nn.Linear(inputSize, hiddenSize)
        self.linear2 = nn.Linear(hiddenSize, outputSize)

    def forward(self, x):
        """
        Not entirly sure... Seems to be a if statement function
        :param x:
        :return:
        """
        x.requires_grad_(True)
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

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
    def __init__(self, lr: float, gamma: float):
        self.lr, self.gama, = lr, gamma

    def trainStep(self, model: PlantModel, replayMemory: ReplayMemory):
        """ Trains the AI Model based on a sample of memories memeories"""
        policyNet = model.copy()
        model.load_state_dict(policyNet.state_dict())
        model.eval()

        optimizer = optim.RMSprop(policyNet.parameters())

        stepsDone = 0

        transitionSample = self._sample(model, ReplayMemory)
        batch = replayMemory.transitions(*zip(*transitionSample))

        nonFinalTrans = torch.tensor(tuple(map(lambda  s: s is not None, batch.nextState)), dtype=torch.bool)
        nonFinalTransNextStates = torch.cat([s for s in batch.nextState if s is not None])

        stateBatch = torch.cat(batch.state)
        actionBatch = torch.cat(batch.action)
        rewardBatch = torch.cat(batch.reward)

        stateActionValues = policyNet(stateBatch).gather(1, actionBatch)
        nextStateValues = torch.zeros(replayMemory.capacity)
        nextStateValues[nonFinalTrans] = model(nonFinalTransNextStates).max(1)[0].detach()

        # Compute teh expected Q Values
        expectedStateActionValues = (nextStateValues * self.gama) + rewardBatch

        # Compute Huber Loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(stateActionValues, expectedStateActionValues.unsqueeze(1))

        # Optiomize the model
        optimizer.zero_grad()
        loss.backward()
        for param in policyNet.parameters():
            param.grad.data.clamp_(-1, 1)
        optimizer.step()


    def _sample(self, model, ReplayMemory):
        if len(ReplayMemory) < model.batchSize:
            return
        return random.sample(ReplayMemory, model.batchSize)




