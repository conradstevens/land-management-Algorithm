import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


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

    def forward(self, x): # TODO/ Function can be deleted?
        """
        Not entirly sure... Seems to be a if statement function
        :param x:
        :return:
        """
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
    def __init__(self, model, lr, gamma):
        self.lr, self.gama, self.model = lr, gamma, model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)  # can be changed for other optimizers
        self.criterion = nn.MSELoss

    def trainStep(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action ,dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Qnew = reward[idx]
            if not done[idx]:
                Qnew = reward[idx] + self.gama * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Qnew

        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.optimizer.step()

