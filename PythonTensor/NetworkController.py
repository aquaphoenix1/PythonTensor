from network.Network import Network
from Locations.Location import Location

from CharacteristicCalculators.Plotter import Plotter

from Levy import Levy
from PathPoint import PathPoint

import numpy as np
import json

class NetworkController(object):
    data = None
    distancesInLocation = None
    distancesBetweenLocation = None
    locationsCount = None

    trainData = None
    trainPoints = None

    generateLocationsArray = None
    generateParametersArray = None
    firstPoints = None

    mostPopularStartLocations = None

    lastLocations = None
    lastLocationsWindow = None
    histCount = None

    Network = Network()

    window = None

    def getWindowSize(self):
        return self.window

    def __init__(self):
        self.data = None
        self.locationsCount = None
        self.mostPopularStartLocations = None

        self.levyCoeff = 4

    def maxTimeCalc(self, data):
        max = data[0][0].time
        min = data[0][0].time
        for arr in data:
            for a in arr:
                if a.time > max:
                    max = a.time
                if a.time < min:
                    min = a.time

        return max, min

    def maxPauseTimeCalc(self, data):
        max = data[0][0].pauseTime
        min = data[0][0].pauseTime
        for arr in data:
            for a in arr:
                if a.pauseTime > max:
                    max = a.pauseTime
                if a.pauseTime < min:
                    min = a.pauseTime

        return max, min

    def setTrainData(self, data, locations, window):
        self.trainPoints = data
        self.locationsCount = len(locations)
        self.distancesInLocation = []
        self.distancesBetweenLocation = []
        self.firstPoints = []
        self.trainStartTimes = []
        self.lastLocations = []
        self.lastLocationsWindow = window
        self.window = window

        self.mostPopularStartLocations = []

        d = []
        num = 0
        for i in data:
            countMostPopular = 0
            locs = [0] * self.locationsCount
            d1 = []
            a = [0] * self.locationsCount
            self.distancesInLocation.append(a.copy())
            self.distancesBetweenLocation.append(a.copy())

            self.firstPoints.append([])

            if not len(self.firstPoints[num]) == self.window:
                self.firstPoints[num].append(i[0].departurePoint)

            for j in i:
                dep = Location.FindLocation(j.departurePoint, locations)
                dest = Location.FindLocation(j.destination, locations)
                d1.append(LocationJump(dep, dest, j.time, j.pauseTime))
                
                if not len(self.firstPoints[num]) == self.window:
                    self.firstPoints[num].append(j.destination)
                if dep.Number == dest.Number:
                    self.distancesInLocation[len(self.distancesInLocation)-1][dep.Number] = self.distancesInLocation[len(self.distancesInLocation)-1][dep.Number] + PathPoint.distanceInMetersBetweenEarthCoordinates(j.departurePoint.latitude, j.departurePoint.longitude, j.destination.latitude, j.destination.longitude)
                else:
                    pass
            d.append(d1)
            num = num + 1
        self.data = d

        self.maxTime, self.minTime = self.maxTimeCalc(data)
        self.maxPauseTime, self.minPauseTime = self.maxPauseTimeCalc(data)

        self.trainData = []

        self.generateLocationsArray = []
        self.generateParametersArray = []

        num = 0

        for arr in self.data:
            if(len(arr) == 0):
                continue
            self.generateLocationsArray.append([])
            self.generateParametersArray.append([])

            x = []
            a = [0] * self.locationsCount
            a[arr[0].departure.Number] = 1
            x.append(a)
            
            if not len(self.generateLocationsArray[num]) == self.window:
                self.generateLocationsArray[num].append(a)

            t = []

            for i in range(len(arr)):
                a = [0] * self.locationsCount
                a[arr[i].destination.Number] = 1
                x.append(a)
                if not len(self.generateLocationsArray[num]) == self.window:
                    self.generateLocationsArray[num].append(a)
                a = [Levy.levyCalculate(arr[i].time, self.minTime, self.maxTime/self.levyCoeff), Levy.levyCalculate(arr[i].pauseTime, self.minPauseTime, self.maxPauseTime / self.levyCoeff)]
                t.append(a)

                if not len(self.generateParametersArray[num]) == self.window - 1:
                    self.generateParametersArray[num].append(a)

            self.trainData.append([x, t])
            num = num + 1

        Plotter.setTrainIntervals(self.trainData, self.distancesInLocation, self.trainPoints, self.locationsCount, self.minTime, self.maxTime, self.minPauseTime, self.maxPauseTime, self.levyCoeff)

        self.histCount = len(Plotter.trainIntervals.tracesLength) + 1 -1 + len(Plotter.trainIntervals.pauseTimes) - 1

    def plotTrain(self):
        Plotter.plotTrained(self.trainData, self.distancesInLocation, self.trainPoints, self.locationsCount, self.minTime, self.maxTime, self.minPauseTime, self.maxPauseTime, self.levyCoeff)

    def plotCharacteristics(self, data):
        Plotter.plot(data, self.locationsCount, self.minTime, self.maxTime, self.minPauseTime, self.maxPauseTime, self.levyCoeff)

    def getTrainData(self):
        return self.data

    def getLocationsCount(self):
        return self.locationsCount;

    def getFeaturesCount(self):
        return 4; #TODO

    def generate(self, locations, parameters):
        count = [0] * len(self.trainData)
        for i in range(len(self.trainData)):
            count[i] = len(self.trainData[i][0]) - self.window ###############################
        result = self.Network.generate(locations, parameters, count, self.firstPoints, self.minPauseTime, self.maxPauseTime, self.levyCoeff)
        self.plotCharacteristics(result)

class LocationJump(object):
    departure = None
    destination = None
    time = None
    pauseTime = None

    def __init__(self, dep, dest, time, pauseTime):
        self.departure = dep
        self.destination = dest
        self.time = time
        self.pauseTime = pauseTime