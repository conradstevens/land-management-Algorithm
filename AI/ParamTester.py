from World.planterMain import Planter
from World.pice import Pice
from AI.masterAI import MasterAI
from AI.plantModel import QtrainerHybrid
from AI.agent import Agent
from AI.replayMemory import ReplayMemory
from AI.piceScorer import DeadPlantScore
import torch
import csv


class ParamTester:
    """ Tests a series of parameters """

    def __init__(self, parameters: list, trainCSV: str, masterAI: MasterAI):
        self.params = parameters
        self.trainCSV = self._openCSV(trainCSV)
        self.mAI = masterAI

    def trainandStore(self):
        """ Runs all sets of parameters and stores the data in the csv"""
        for p in parameters:
            scores, lossCount = self.runMasterAI(p[0], p[1], p[2])
            self.appendData(p[0], p[1], p[2], scores, lossCount)

    def runMasterAI(self, viewDistance, hiddenLayer, epsilon):
        """ Runs a single set of parameters and returns the data """
        planter = Planter(bagSize=400, viewDistance=viewDistance, pice=Pice(trainingPices[0]))
        score = DeadPlantScore(planter)
        agent = Agent(planter, score)

        self.mAI = MasterAI(agent=agent,
                            trainer=self.mAI.trainer,
                            trainingPices=self.mAI.trainingPices,
                            hiddenSize1=hiddenLayer,
                            lr=self.mAI.lr,
                            epsilon=self.mAI.epsilon,
                            nEpochs=self.mAI.nEpochs,
                            replayMemory=ReplayMemory(capacity=10_000),
                            showEvery=self.mAI.showEvery,
                            printEvery=self.mAI.printEvery,
                            renderSleep=self.mAI.renderSleep,
                            modelName=self.mAI.modelNameOriginal,  # subject to change
                            model=None,  # model=model)
                            doShowCharts=False,
                            doRender=False)

        self.mAI.runAi()
        return self.mAI.scores, self.mAI.lossCount

    def appendData(self, viewD: int, hdLayer: int, epsilon: float, scores: list, lossCount: list):
        """ Appends the data to the CSV  """
        for i in range(0, len(scores)):
            writer = csv.writer(self.trainCSV)
            writer.writerow([i, viewD, hdLayer, epsilon, scores[i], lossCount[i]])

    def _openCSV(self, trainCsv):
        """ Open CSV and set it up to have data entered to it """
        trainCsv = open(trainCsv, 'w', newline='')
        trainCsv.truncate(0)

        writer = csv.writer(trainCsv)
        writer.writerow(['Epoch', 'View Distance', 'Hidden Layer Size', 'Epsilon', 'Score', 'Loss'])

        return trainCsv


if __name__ == '__main__':
    viewDistance = [1, 2]
    hiddenLayerSize = [16, 32, 64]
    epsilon = [0.8, 0.999999999]
    CSVFname = 'C:/Users/conra/Documents/land-management-Algorithm/AI/Models/Train1.csv'
    parameters = [(v, h, g) for v in viewDistance for h in hiddenLayerSize for g in epsilon]

    trainingPices = ['C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train0.txt']
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train0.txt',  # 19
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train1.txt',  # 20
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train2.txt',  # 19
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train3.txt',  # 16
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train4.txt',  # 17
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train5.txt',  # 18
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train6.txt',  # 16
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train7.txt',  # 15
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train8.txt',  # 18
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train9.txt',  # 20
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train10.txt', # 14
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train11.txt', # 19
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train12.txt', # 20
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train13.txt', # 19
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train14.txt', # 17
    # 'C:/Users/conra/Documents/land-management-Algorithm/World/Pices/RowTrainRoads1/Train15.txt'] # 17

    # model = torch.load('C:/Users/conra/Documents/land-management-Algorithm/AI/Models/QtrainHybridStart_View2')
    planter = Planter(bagSize=400, viewDistance=2, pice=Pice(trainingPices[0]))
    score = DeadPlantScore(planter)
    trainer = QtrainerHybrid(batchSize=500, scoreExpectation=19)
    agent = Agent(planter, score)

    masterAi = MasterAI(agent=agent,
                        trainer=trainer,
                        trainingPices=trainingPices,
                        hiddenSize1=32,
                        lr=0.01,
                        epsilon=0.999999999,  # Chance not to make random move
                        nEpochs=10_000,
                        replayMemory=ReplayMemory(capacity=10_000),
                        showEvery=1_000,
                        printEvery=1,
                        renderSleep=0.1,
                        modelName="ParamTestRunModels/QtrainHybridStart",
                        model=None,  # model=model)
                        doShowCharts=False)

    paramTester = ParamTester(parameters, CSVFname, masterAi)
    paramTester.trainandStore()