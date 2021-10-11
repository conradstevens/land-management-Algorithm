from collections import namedtuple, deque
import random


class ReplayMemory(object):
    """ A class to manage all the transition memories of the planter has seen """

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = deque([], maxlen=capacity)
        self.transitions = namedtuple('Transition', ('state', 'action', 'nextState', 'reward', 'done'))

    def push(self, *args):
        """Save a transition"""
        self.memory.append(self.transitions(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def clear(self):
        self.memory = deque([], maxlen=self.capacity)

    def __len__(self):
        return len(self.memory)
