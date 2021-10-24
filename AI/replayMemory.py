from collections import namedtuple, deque
import random
import torch


class ReplayMemory(object):
    """ A class to manage all the transition memories of the planter has seen """

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = deque([], maxlen=capacity)
        self.transitions = namedtuple('Transition', ('state', 'surround', 'action',
                                                     'nextState', 'reward', 'move', 'done'))

    def push(self, curState, surround, action, nextState, reward, move, finished):
        """Save a transition"""
        self.memory.append(self.transitions(curState, surround, action, nextState, reward, move, finished))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def clear(self):
        self.memory = deque([], maxlen=self.capacity)

    def __len__(self):
        return len(self.memory)

