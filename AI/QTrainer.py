import torch
import random

class QTrainer:
    def __init__(self, gama, lr, epsilon, maxMemory):
        self.gama, self.lr, self.epsilon, self.maxMemory = gama, lr, epsilon, maxMemory
        self.qList = {}

    def getAction(self, state, doRand):
        """
        Returns the action of the planter based of the state
        If the state is not in the Qtable then will a random state
        # TODO Back Propogation
        """
        if doRand:
            return random.randint(0, 3)
        elm = self.getElm(state)
        return elm.getStateAction()

    def getElm(self, state):
        """ :return: tensor element with state
        :rtype: QlistElm"""
        if not state in self.qList:
            elm = QlistElm(state)
            self.qList.update(elm.getDicElm())
            return elm
        return self.qList.get(state)

    def learn(self, oldState: tuple, newStae: tuple, reward: float):
        """ training step applied to action """
        oldQElm = self.getElm(oldState)
        newQElm = self.getElm(newStae)
        maxOldQ = oldQElm.getMaxWeight()
        maxNewQ = newQElm.getMaxWeight()

        newQ = (1 - self.lr) * maxOldQ + self.lr * (reward + self.gama * maxNewQ)
        oldQElm.setMaxWeight(newQ)


class QlistElm:
    """ An element in the Qlist """

    def __init__(self, state):
        """
        :param state: state planter is in
        actionW: list of weights for each possible action
        """
        self.state = state
        self.actionW = torch.rand(4)

    def getDicElm(self):
        return {self.state: self}

    def getStateAction(self):
        """ returns the move tensor and returns applies the back propagation
        int (0, 1, 2, 3) """
        return torch.argmax(self.actionW).item()

    def getMaxWeight(self):
        """ :return max weight of actionW tensor """
        return self.actionW.max().item()

    def setMaxWeight(self, newQ: float):
        """ Sets the max weight of the tensor """
        actionNum = self.getStateAction()
        self.actionW[actionNum] = newQ
