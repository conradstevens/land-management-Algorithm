from AI.Agent import Agent
from AI.Agent import PiceRunner
from AI.PlantModel import PlantModel
from AI.PlantModel import Qtrainer
from tests.Tester import getBasic_Pice_and_Planter
from AI.PiceScorer import PiceScore
from AI.Stats import Stats
import PiceClasses.Pice
from PlanterClasses.PlanterMain import Planter
from collections import deque
import time

MAX_MEMORY = 100_000

class MasterAI:
    """
    Oversees Agent and trainer,
    creating and working models.
    TODO/ To be trained?
    TODO/ Refactor to run different models
    """

    def __init__(self, agent: Agent, piceRunner: PiceRunner, gama: float, lr: float):
        self.agent, self.piceRunner = agent, piceRunner

        self.stats = Stats(self.agent.planter.pice.window)
        self.piceScore = PiceScore(planter)

        self.model = PlantModel(self.agent.inputSize, agent.inputSize, 4)
        self.trainer = Qtrainer(self.model, lr, gama)
        self.memory = deque(maxlen=MAX_MEMORY)

    def playPice(self):
        """
        runs through the pice with the current model
        """
        self.stats.drawStats()
        while not agent.planter.finished:
            curState = self.agent.inputTensor
            action = self.piceRunner.playPice(self.model, self.chanceofRandMove())  # Moves pice and gets move as tensor
            self.piceScore.scorePice()
            deltaScore = self.piceScore.deltaScore
            nextState = self.agent.getInputTensor()

            self.trainer.trainStep(state=curState,
                                   action=action,
                                   reward=deltaScore,
                                   nextState=nextState,
                                   done=planter.finished)

            self._remember(curState, action, deltaScore, nextState, planter.finished)

            time.sleep(1)

    def _remember(self, state, move, reward, nextState, done):
        """
        Records each move and associated reward
        """
        self.memory.append((state, move, reward, nextState, done))


    def chanceofRandMove(self):
        return (80 - self.stats.nGames) / 200


if __name__ == '__main__':
    # pice, planter = getBasic_Pice_and_Planter()
    pice = PiceClasses.Pice.PiceWind('C:/Users/conra/Documents/land-management-Algorithm/PiceClasses/Pices/Pice1.txt', 12)
    planter = Planter(400, 3, pice)


    agent = Agent(planter)
    piceRunner = PiceRunner(agent)
    masterAi = MasterAI(agent, piceRunner, gama=0.9, lr=0.1)
    masterAi.playPice()