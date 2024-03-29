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


class Trainer:
    """ Template for training models"""
    def __init__(self):
        pass


class Qtrainer(Trainer):
    """ Trains the AI based on samples of states it encounters """
    def __init__(self, batchSize):
        super().__init__()
        self.batchSize = batchSize

    def trainStep(self, model: PlantModel, replayMemory: ReplayMemory, score=None):
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
        if loss == 0:  # Prevents slightly tweaking weights when loss is zero
            return loss.item()
        loss.backward()  # Back propagates
        model.opt.step()  # optimizes

        return loss.item()

    def _sample(self, model, replayMemory: ReplayMemory):
        if len(replayMemory) < self.batchSize:
            return replayMemory.sampleMoveData(len(replayMemory))
        return replayMemory.sampleMoveData(self.batchSize)

    def _getReward(self, surroundings, move):
        """ Returns is the move was profitable"""
        return surroundings[move.item()]


class QtrainerHybrid(Qtrainer):
    """ Trains the AI based on samples of states it encounters """
    def __init__(self, batchSize, scoreExpectation=None):
        super().__init__(batchSize)
        self.batchSize = batchSize
        self.scoreExpectation = scoreExpectation

    def trainStep(self, model: PlantModel, replayMemory: ReplayMemory, score=None):
        """ Trains the AI Model based on a sample of memories memeories """
        model.opt.zero_grad()  # Zeros the gradients collected while training and getting data

        transitionSample = replayMemory.memory  # Gets a larger random sample of moves
        batch = replayMemory.transitions(*zip(*transitionSample))  # Organizes the sample as a named tuple

        stateBatch = torch.stack([s for s in batch.state])  # Gets a stack of states
        surroundBatch = torch.stack([s for s in batch.surround])  # Gets a stack of left right up down
        doneMask = torch.stack([torch.tensor([0]) if s else torch.tensor([1]) for s in batch.done])  # Gets a stack of if this was the last move

        qEval = model.forward(stateBatch)  # Evaluates the nn's moves for each state
        baseline = torch.stack([torch.tensor([1]) for i in batch.state])  # stacks an assumed base line of a perfect score [1, 1..., 1]

        evalMoves = torch.stack([torch.tensor([qval.argmax().item()]) for qval in qEval])  # Evaluates the Q-score / certainty of each move
        rewards = torch.stack([torch.tensor([self._getReward(surroundBatch[i], evalMoves[i])])  # Determines returns the profitability of each move
                               for i in range(0, len(evalMoves))])

        loss = torch.sum(torch.log(qEval) * doneMask * (rewards - baseline)) * (self.scoreExpectation - score)  # Loss Calculation - Will calculate greater change is less certain of a Q-Score
        if loss == 0:  # Prevents slightly tweaking weights when loss is zero
            return loss.item()
        loss.backward()  # Back propagates
        model.opt.step()  # optimizes

        replayMemory.clearMoveData()  # Clears move data so that each epoch is treated independently
        return loss.item()


class PiceTrainer(Trainer):
    """ Trains the AI based on the final score of the pice it gets """
    def __init__(self, batchSize):
        super().__init__()

    def trainStep(self, model: PlantModel, replayMemory: ReplayMemory, deadCount: float):
        """ Trains the model with loss calculated only when the pice has been complete / abandoned"""
        model.opt.zero_grad()  # Zeros the gradients collected while training and getting data
        if deadCount == 0:  # Training on zero still tweaking the net slightly
            return 0

        stateBatch = torch.stack([i.state for i in replayMemory.memory])  # Gets a stack of states
        qEval = model.forward(stateBatch)  # Evaluates the nn's moves for each state

        loss = torch.sum(torch.log(qEval) * -deadCount)
        loss.backward()

        model.opt.step()
        replayMemory.clearMoveData()

        return loss.item()