from collections import namedtuple, deque
import random


class ReplayMemory(object):
    """ A class to manage all the transition memories of the planter has seen """

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = deque([], maxlen=capacity)
        self.piceScore = 0
        self.transitions = namedtuple('Transition', ('state', 'surround', 'action',
                                                     'nextState', 'reward', 'move', 'done'))

    def moveDataPush(self, curState, surround, action, nextState, reward, move, finished):
        """Save a transition"""
        self.memory.append(self.transitions(curState, surround, action, nextState, reward, move, finished))

    def sampleMoveData(self, batch_size):
        return random.sample(self.memory, batch_size)

    def clearMoveData(self):
        self.memory = deque([], maxlen=self.capacity)

    def __len__(self):
        return len(self.memory)

