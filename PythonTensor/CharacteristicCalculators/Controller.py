import numpy as np
from PathPoint import PathPoint

class Controller(object):
    @staticmethod
    def calculate(dataLocations, dataParameters, traceNumber, distancesInLocation, isTrain=False):
        return [PlotClass('Длины трасс в локациях ' + str(traceNumber), Controller.calculateTracesLength(dataLocations, distancesInLocation, isTrain)),
                PlotClass('Длины прыжков ' + str(traceNumber), Controller.calculateJumpLength(dataLocations, distancesInLocation, isTrain)), 
                PlotClass('Время паузы ' + str(traceNumber), Controller.calculatePauseTime(dataLocations, dataParameters)), 
                PlotClass('Количество посещений локации ' + str(traceNumber), Controller.calculateCountLocation(dataLocations))]

    @staticmethod
    def calculateJumpLength(dataLocations, distances, isTrain):
        if isTrain == True:
            return distances

        res = [0] * len(dataLocations[0])

        for i in range(len(dataLocations) - 1):
            if not np.argmax(dataLocations[i]) == np.argmax(dataLocations[i+1]):
                res[np.argmax(dataLocations[i])] = res[np.argmax(dataLocations[i])] + PathPoint.distanceInMetersBetweenEarthCoordinates(distances[i].latitude, distances[i].longitude, distances[i+1].latitude, distances[i+1].longitude)

        return res

    @staticmethod
    def calculateAllTime(traces):
        res = []

        for i in range(len(traces)):
            r = 0
            for j in traces[i][1]:
                r = r + j[0] + j[1]
            res.append(r)

        return PlotClass('Время прохождение трасс', res)

    @staticmethod
    def calculateTracesLength(dataLocations, distances, isTrain):
        if isTrain == True:
            return distances

        res = [0] * len(dataLocations[0])

        for i in range(len(dataLocations) - 1):
            if np.argmax(dataLocations[i]) == np.argmax(dataLocations[i+1]):
                res[np.argmax(dataLocations[i])] = res[np.argmax(dataLocations[i])] + PathPoint.distanceInMetersBetweenEarthCoordinates(distances[i].latitude, distances[i].longitude, distances[i+1].latitude, distances[i+1].longitude)

        return res

    @staticmethod
    def calculatePauseTime(dataLocations, dataParameters):
        res = [0] * len(dataLocations[0])

        for i in range(len(dataParameters)):
            res[dataLocations[i+1].index(1)] = res[dataLocations[i+1].index(1)] + dataParameters[i][1]

        return res

    @staticmethod
    def calculateCountLocation(dataLocations):
        res = [0] * len(dataLocations[0])

        for i in range(len(dataLocations)):
            res[dataLocations[i].index(1)] = res[dataLocations[i].index(1)] + 1

        return res

class PlotClass(object):
    label = None
    data = None

    def __init__(self, label, data):
        self.label = label
        self.data = data