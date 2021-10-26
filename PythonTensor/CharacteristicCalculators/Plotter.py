import matplotlib.pyplot as plt
import numpy as np
from CharacteristicCalculators.Controller import Controller

class Plotter(object):
    @staticmethod
    def plotTrain(data):
        Plotter.plot(data)

    @staticmethod
    def plot(train, data, distancesInLocation, distancesBetweenLocation):
        for i in range(len(data)):
            calcTrained = Controller.calculate(train[i][0], train[i][1], i, distancesInLocation[i], True)
            calcPredicted = Controller.calculate(data[i][0], data[i][1], i, data[i][2])
            for k in range(len(calcTrained)):
                x = np.arange(len(calcTrained[k].data))
                Plotter.plotData(x, calcTrained[k].data, calcPredicted[k].data, calcTrained[k].label)

        calcTrained = Controller.calculateAllTime(train)
        calcPredicted = Controller.calculateAllTime(data)
        Plotter.plotData(np.arange(len(calcTrained.data)), calcTrained.data, calcPredicted.data, calcTrained.label)

    @staticmethod
    def plotData(x, data1, data2=None, yLabel='', width = 0.35):
        fig, ax = plt.subplots(figsize=(40,5))
        ax.bar(x-width/2, data1, width, label='trained')
        if not data2 == None:
            ax.bar(x+width/2, data2, width, label='predicted')
        ax.set_ylabel(yLabel)
        ax.set_xticks(x)
        ax.legend()