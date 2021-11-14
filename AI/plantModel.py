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
            nn.Sigmoid(),
            nn.Linear(hiddenSize, outputSize),
            nn.Softmax(dim=-1)
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
        model.opt.zero_grad()  # Zeros the gradients collected while training and getting data

        transitionSample = self._sample(model, replayMemory)  # Gets a larger random sample of moves
        batch = replayMemory.transitions(*zip(*transitionSample))  # Organizes the sample as a named tuple

        stateBatch = torch.stack([s for s in batch.state])  # Gets a stack of states
        surroundBatch = torch.stack([s for s in batch.surround])  # Gets a stack of left right up down
        doneMask = torch.stack([torch.tensor([0]) if s else torch.tensor([1]) for s in batch.done]) # Gets a stack of if this was the last move

        qEval = model.forward(stateBatch)  # Evaluates the nn's moves for each state
        baseline = torch.stack([torch.tensor([1]) for i in batch.state])  # stacks an assumed base line of a perfect score [1, 1..., 1]

        evalMoves = torch.stack([torch.tensor([qval.argmax().item()]) for qval in qEval])  # Evaluates the Q-score / certainty of each move
        rewards = torch.stack([torch.tensor([self._getReward(surroundBatch[i], evalMoves[i])])  # Determines returns the profitability of each move
                               for i in range(0, len(evalMoves))])

        loss = torch.sum(torch.log(qEval) * doneMask * (rewards - baseline))  # Loss Calculation - Will calculate greater change is less certain of a Q-Score
        loss.backward()  # Back propagates
        model.opt.step()  # optimizes

    def _sample(self, model, replayMemory: ReplayMemory):
        if len(replayMemory) < self.batchSize:
            return replayMemory.sample(len(replayMemory))
        return replayMemory.sample(self.batchSize)

    def _getReward(self, surroundings, move):
        """ Returns is the move was profitable"""
        return surroundings[move.item()]

