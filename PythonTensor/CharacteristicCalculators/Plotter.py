import matplotlib.pyplot as plt
import numpy as np
from CharacteristicCalculators.Controller import Controller
import sys
from PathPoint import PathPoint
from Jump import Jump
from Levy import Levy
import math

import json
from json import JSONEncoder

class Intervals:
    def __init__(self):
        self.tracesLength = None

class Plotter(object):
    generatedData = []
    intervalsCount = 20
    minInInterval = 5

    maxTraceTime = None

    trainIntervals = Intervals()

    fig = None
    ax = None
    bar = None

    @staticmethod
    def initFigure():
        Plotter.fig, Plotter.ax = plt.subplots()
        return Plotter.fig

    @staticmethod
    def getTrained():
        return Plotter.trainedCountLocations, Plotter.trainIntervals.countLocations

    @staticmethod
    def appendData(data):
        Plotter.generatedData.append(data)

    @staticmethod
    def plotG(index, locationsCount, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff):
        x = None
        if index == 0:
            x = Plotter.trainIntervals.tracesLength
            for j in range(len(Plotter.generatedData)):
                distancesInLocation = []
                for i in range(len(Plotter.generatedData[j])):
                    distancesInLocation.append([0] * locationsCount)
                    for k in range(len(Plotter.generatedData[j][i][0]) - 1):
                        if Plotter.generatedData[j][i][0][k].index(1) == Plotter.generatedData[j][i][0][k+1].index(1):
                            distancesInLocation[i][Plotter.generatedData[j][i][0][k].index(1)] += PathPoint.distanceInMetersBetweenEarthCoordinates(Plotter.generatedData[j][i][2][k].latitude, Plotter.generatedData[j][i][2][k].longitude, Plotter.generatedData[j][i][2][k+1].latitude, Plotter.generatedData[j][i][2][k+1].longitude)
                trained, _ = Plotter.calculateTracesLength(distancesInLocation, False)

                hist = np.histogram(trained, bins=x, density=True)[0]
                bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
                Plotter.ax.plot(bin_centers, hist, label = 'generated' + str(j))
        elif index == 1:
            x = Plotter.trainIntervals.tracesTime

            for j in range(len(Plotter.generatedData)):
                trained, _ = Plotter.tracesTime(Plotter.generatedData[j], minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, False)
                hist = np.histogram(trained, bins=x, density=True)[0]
                bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
                Plotter.ax.plot(bin_centers, hist, label = 'generated' + str(j))
        elif index == 2:
            x = Plotter.trainIntervals.jumpLength

            for j in range(len(Plotter.generatedData)):
                jumps = []
                for i in Plotter.generatedData[j]:
                    j1 = []
                    for k in range(len(i[2]) - 1):
                        j1.append(Jump(i[2][k], i[2][k+1], 0, 0))
                    jumps.append(j1)

                trained, _ = Plotter.calculateJumpLength(jumps)
                hist = np.histogram(trained, bins=x, density=True)[0]
                bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
                Plotter.ax.plot(bin_centers, hist, label = 'generated' + str(j))
        elif index == 3:
            x = Plotter.trainIntervals.pauseTimes
            for j in range(len(Plotter.generatedData)):
                trained, _ = Plotter.calculatePauseTimes(Plotter.generatedData[j], minPauseTime, maxPauseTime, levyCoeff, False)
                hist = np.histogram(trained, bins=x, density=True)[0]
                bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
                Plotter.ax.plot(bin_centers, hist, label = 'generated' + str(j))
        elif index == 4:
            x = np.arange(locationsCount)
            for j in range(len(Plotter.generatedData)):
                trained, _ = Plotter.calculateLocationsCount(Plotter.generatedData[j], locationsCount)
                #Plotter.ax.bar(x, height=trained)
                Plotter.ax.plot(x, trained, label = 'generated' + str(j))
        elif index == 5:
            x = Plotter.trainIntervals.unique
            for j in range(len(Plotter.generatedData)):
                trained, _ = Plotter.calculateDifferentLocationsCount(Plotter.generatedData[j], locationsCount)
                hist = np.histogram(trained, bins=x, density=True)[0]
                bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
                Plotter.ax.plot(bin_centers, hist, label = 'generated' + str(j))

        Plotter.ax.legend()
        Plotter.ax.set_xticks(x)


    @staticmethod
    def plotT(index):
        x = None
        if index == 0:
            x = Plotter.trainIntervals.tracesLength
            hist = np.histogram(Plotter.trainedLengthInTraces, bins=x, density=True)[0]
            bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
            Plotter.ax.plot(bin_centers, hist, label = 'trained')
        elif index == 1:
            x = Plotter.trainIntervals.tracesTime
            hist = np.histogram(Plotter.trainedTime, bins=x, density=True)[0]
            bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
            Plotter.ax.plot(bin_centers, hist, label = 'trained')
        elif index == 2:
            x = Plotter.trainIntervals.jumpLength
            hist = np.histogram(Plotter.trainedJumpLength, bins=x, density=True)[0]
            bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
            Plotter.ax.plot(bin_centers, hist, label = 'trained')
        elif index == 3:
            x = Plotter.trainIntervals.pauseTimes
            hist = np.histogram(Plotter.trainedPauseTime, bins=x, density=True)[0]
            bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
            Plotter.ax.plot(bin_centers, hist, label = 'trained')
        elif index == 4:
            x = Plotter.trainIntervals.countLocations
            Plotter.ax.plot(x, Plotter.trainedCountLocations, label = 'trained')
            #Plotter.ax.bar(x, height=Plotter.trainedCountLocations)
        elif index == 5:
            x = Plotter.trainIntervals.unique
            hist = np.histogram(Plotter.trainedUnique, bins=x, density=True)[0]
            bin_centers = 0.5*(np.array(x[1:])+np.array(x[:-1]))
            Plotter.ax.plot(bin_centers, hist, label = 'trained')
            
        Plotter.ax.set_xticks(x)
        Plotter.ax.legend()

    @staticmethod
    def clear():
        Plotter.clearGraph()
        Plotter.generatedData = []

    @staticmethod
    def clearGraph():
        Plotter.ax.cla()

    @staticmethod
    def setTrainIntervals(train, distancesInLocation, trainPoints, locationsCount, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff):
        Plotter.trainedCountLocations, it = Plotter.calculateLocationsCount(train, locationsCount)
        Plotter.trainIntervals.countLocations = it

        Plotter.trainedLengthInTraces, it = Plotter.calculateTracesLength(distancesInLocation)
        Plotter.trainIntervals.tracesLength = it

        trained, it = Plotter.tracesTime(train, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff)
        Plotter.trainIntervals.tracesTime = it

        Plotter.maxTraceTime = max(trained)

        Plotter.trainedTime = trained

        Plotter.trainedPauseTime, it = Plotter.calculatePauseTimes(train, minPauseTime, maxPauseTime, levyCoeff)
        Plotter.trainIntervals.pauseTimes = it

        Plotter.trainedJumpLength, it = Plotter.calculateJumpLength(trainPoints)
        Plotter.trainIntervals.jumpLength = it

        Plotter.trainedUnique, it = Plotter.calculateDifferentLocationsCount(train, locationsCount)
        Plotter.trainIntervals.unique = it

    class SaveData(object):{
        }

    @staticmethod 
    def plotTrained(train, distancesInLocation, trainPoints, locationsCount, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff):
        saveData = Plotter.SaveData()

        trained, _ = Plotter.calculateTracesLength(distancesInLocation, False)
        saveData.TracesLengthInLocation = Plotter.plotData(Plotter.trainIntervals.tracesLength, trained, 'Длины трасс в локациях при обучении')

        saveData.TracesLengthInLocationIntervals = Plotter.trainIntervals.tracesLength
        
        trained, _ = Plotter.tracesTime(train, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, False)
        saveData.TracesTime = Plotter.plotData(Plotter.trainIntervals.tracesTime, trained, 'Время прохождения трасс при обучении')

        saveData.TracesTimeIntervals = Plotter.trainIntervals.tracesTime

        trained, _ = Plotter.calculateJumpLength(trainPoints, False)
        saveData.JumpLength = Plotter.plotData(Plotter.trainIntervals.jumpLength, trained, 'Длины прыжков при обучении')

        saveData.JumpLengthIntervals = Plotter.trainIntervals.jumpLength

        trained, _ = Plotter.calculatePauseTimes(train, minPauseTime, maxPauseTime, levyCoeff, False)
        saveData.PausesTime = Plotter.plotData(Plotter.trainIntervals.pauseTimes, trained, 'Время пауз при обучении')

        saveData.PausesTimeIntervals = Plotter.trainIntervals.pauseTimes

        trained, it = Plotter.calculateLocationsCount(train, locationsCount)
        saveData.LocationsCount = Plotter.plotBar(it, trained, 'Количество посещений локаций при обучении')

        saveData.LocationsCountIntervals = list(it)

        trained, _ = Plotter.calculateDifferentLocationsCount(train, locationsCount, False)
        saveData.DifferentLocations = Plotter.plotData(Plotter.trainIntervals.unique, trained, 'Уникальные локации при обучении')

        saveData.DifferentLocationsIntervals = Plotter.trainIntervals.unique

        with open('trained.txt', 'w+') as f:
            json.dump({"TracesLengthInLocation": str(saveData.TracesLengthInLocation),
                       "TracesLengthInLocationIntervals": str(saveData.TracesLengthInLocationIntervals),
                       "TracesTime": str(saveData.TracesTime),
                       "TracesTimeIntervals": str(saveData.TracesTimeIntervals),
                       "JumpLength": str(saveData.JumpLength),
                       "JumpLengthIntervals": str(saveData.JumpLengthIntervals),
                       "PausesTime": str(saveData.PausesTime),
                       "PausesTimeIntervals": str(saveData.PausesTimeIntervals),
                       "LocationsCount": str(saveData.LocationsCount),
                       "LocationsCountIntervals": str(saveData.LocationsCountIntervals),
                       "DifferentLocations": str(saveData.DifferentLocations),
                       "DifferentLocationsIntervals": str(saveData.DifferentLocationsIntervals)
                       }, f)

    @staticmethod
    def plot(data, locationsCount, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, name=''):
        saveData = Plotter.SaveData()

        distancesInLocation = []
        for i in range(len(data)):
            distancesInLocation.append([0] * locationsCount)
            for k in range(len(data[i][0]) - 1):
                if data[i][0][k].index(1) == data[i][0][k+1].index(1):
                    distancesInLocation[i][data[i][0][k].index(1)] += PathPoint.distanceInMetersBetweenEarthCoordinates(data[i][2][k].latitude, data[i][2][k].longitude, data[i][2][k+1].latitude, data[i][2][k+1].longitude)
        trained, _ = Plotter.calculateTracesLength(distancesInLocation, False)
        saveData.TracesLengthInLocation = Plotter.plotData(Plotter.trainIntervals.tracesLength, trained, 'Длины трасс в локациях при генерации ' + name)
        
        saveData.TracesLengthInLocationIntervals = Plotter.trainIntervals.tracesLength

        trained, _ = Plotter.tracesTime(data, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, False)
        saveData.TracesTime = Plotter.plotData(Plotter.trainIntervals.tracesTime, trained, 'Время прохождения трасс при генерации ' + name)

        saveData.TracesTimeIntervals = Plotter.trainIntervals.tracesTime

        jumps = []
        for i in data:
            j = []
            for k in range(0, len(i[2]) - 1, 2): ######################### delete 2
                j.append(Jump(i[2][k], i[2][k+1], 0, 0))
            jumps.append(j)

        trained, _ = Plotter.calculateJumpLength(jumps)
        saveData.JumpLength = Plotter.plotData(Plotter.trainIntervals.jumpLength, trained, 'Длины прыжков при генерации ' + name)

        saveData.JumpLengthIntervals = Plotter.trainIntervals.jumpLength

        trained, _ = Plotter.calculatePauseTimes(data, minPauseTime, maxPauseTime, levyCoeff, False)
        saveData.PausesTime = Plotter.plotData(Plotter.trainIntervals.pauseTimes, trained, 'Время пауз при генерации ' + name)

        saveData.PausesTimeIntervals = Plotter.trainIntervals.pauseTimes

        trained, it = Plotter.calculateLocationsCount(data, locationsCount)
        saveData.LocationsCount = Plotter.plotBar(it, trained, 'Количество посещений локаций при генерации ' + name)

        saveData.LocationsCountIntervals = list(it)

        trained, _ = Plotter.calculateDifferentLocationsCount(data, locationsCount)
        saveData.DifferentLocations = Plotter.plotData(Plotter.trainIntervals.unique, trained, 'Уникальные локации при генерации ' + name)

        saveData.DifferentLocationsIntervals = Plotter.trainIntervals.unique

        with open('generated.txt', 'w+') as f:
            json.dump({"TracesLengthInLocation": str(saveData.TracesLengthInLocation),
                       "TracesLengthInLocationIntervals": str(saveData.TracesLengthInLocationIntervals),
                       "TracesTime": str(saveData.TracesTime),
                       "TracesTimeIntervals": str(saveData.TracesTimeIntervals),
                       "JumpLength": str(saveData.JumpLength),
                       "JumpLengthIntervals": str(saveData.JumpLengthIntervals),
                       "PausesTime": str(saveData.PausesTime),
                       "PausesTimeIntervals": str(saveData.PausesTimeIntervals),
                       "LocationsCount": str(saveData.LocationsCount),
                       "LocationsCountIntervals": str(saveData.LocationsCountIntervals),
                       "DifferentLocations": str(saveData.DifferentLocations),
                       "DifferentLocationsIntervals": str(saveData.DifferentLocationsIntervals)
                       }, f)
        
    @staticmethod
    def calculateDifferentLocationsCount(train, locationsCount, isCountIntervals = True):
        trainResult = []
        
        for i in train:
            arr = [0] * locationsCount
            for j in i[0]:
                arr[j.index(1)] = 1
            trainResult.append(arr)

        trainResult = list(np.asarray(trainResult).sum(axis=1))

        intervals = None

        if isCountIntervals == True:
            maxVal = max(trainResult)
            minVal = min(trainResult)

            intervals = Plotter.getIntervals(minVal, maxVal)

            Plotter.minOperationsByDividing(trainResult, intervals)

        return trainResult, intervals


    @staticmethod
    def getIntervals(min, max):
        return [min, (max+min) / 2, max]

    @staticmethod
    def tracesTime(train, minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, isCalcIntervals = True):
        trainTimes = []
        for i in train:
            time = 0
            for j in i[1]:
                time = time + Levy.restoreLevy(j[0], minTime, maxTime/levyCoeff) + Levy.restoreLevy(j[1], minPauseTime, maxPauseTime/levyCoeff)
            
            if not math.isnan(time):
                trainTimes.append(time)

        intervals = None

        if isCalcIntervals == True:
            maxVal = max(trainTimes)
            minVal = min(trainTimes)

            intervals = Plotter.getIntervals(minVal, maxVal)

            Plotter.minOperationsByDividing(trainTimes, intervals)

        return trainTimes, intervals

    @staticmethod
    def calculateLocationsCount(train, locationsCount):
        resTrained = [0] * locationsCount

        for i in train:
            for j in i[0]:
                resTrained[j.index(1)] = resTrained[j.index(1)] + 1

        return resTrained, np.arange(locationsCount)

    @staticmethod
    def calculatePauseTimes(train, minPauseTime, maxPauseTime, levyCoeff, isCalcIntervals = True):
        allPausesTrained = []
        for i in train:
            pausesRows = [row[1] for row in i[1]]
            allPausesTrained = allPausesTrained + pausesRows

        for i in range(len(allPausesTrained)):
            allPausesTrained[i] = Levy.restoreLevy(allPausesTrained[i], minPauseTime, maxPauseTime/levyCoeff)

        intervals = None

        if isCalcIntervals == True:
            minVal = min(allPausesTrained)
            maxVal = max(allPausesTrained)

            intervals = Plotter.getIntervals(minVal, maxVal)
        
            Plotter.minOperationsByDividing(allPausesTrained, intervals)

        return allPausesTrained, intervals
        
    @staticmethod
    def calculateJumpLength(distancesInTrainLocation, isCalcIntervals = True):
        distancesTrained = []

        for i in distancesInTrainLocation:
            for k in i:
                distancesTrained.append(PathPoint.distanceInMetersBetweenEarthCoordinates(k.departurePoint.latitude, k.departurePoint.longitude, k.destination.latitude, k.destination.longitude))

        #for i in data:
        #    for k in range(len(i[2])-1):
        #        if not np.argmax(i[0][k]) == np.argmax(i[0][k+1]):
        #            firstPoint = i[2][k]
        #            secondPoint = i[2][k+1]
        #            distancesPredicted.append(PathPoint.distanceInMetersBetweenEarthCoordinates(firstPoint.latitude, firstPoint.longitude, secondPoint.latitude, secondPoint.longitude))

        intervals = None
        if isCalcIntervals == True:
            maxVal = max(distancesTrained)
            minVal = min(distancesTrained)

            intervals = Plotter.getIntervals(minVal, maxVal)

            Plotter.minOperationsByDividing(distancesTrained, intervals)

        return distancesTrained, intervals

    @staticmethod
    def calculateTracesLength(distancesInTrainLocation, isCalcIntervals = True):
        #distancesPredicted = []
        #for k in data:
        #    el = k[0]
        #    res = [0] * len(el[0])

        #    for i in range(len(el) - 1):
        #        if np.argmax(el[i]) == np.argmax(el[i+1]):
        #            res[np.argmax(el[i])] = res[np.argmax(el[i])] + PathPoint.distanceInMetersBetweenEarthCoordinates(k[2][i].latitude, k[2][i].longitude, k[2][i+1].latitude, k[2][i+1].longitude)
        #    distancesPredicted.append(res)

        allDistances = []

        for i in range(len(distancesInTrainLocation)):
            allDistances = allDistances + [k for k in distancesInTrainLocation[i] if k != 0]

        intervals = None

        if isCalcIntervals == True:
            if len(allDistances) == 0:
                return allDistances, []
            minVal = min(allDistances)
            maxVal = max(allDistances)

            intervals = Plotter.getIntervals(minVal, maxVal)

            Plotter.minOperationsByDividing(allDistances, intervals)

        return allDistances, intervals

    @staticmethod
    def minOperations(arr, K, intervals):
        #index = size
        #while (index > 0):
        #    least = arr[index]
        #    if least < K:
        #        second_least = arr[index-1]
        #        del arr[index]
        #        del arr[index-1]
        #        arr.insert(index-1, least + second_least)

        #        del intervals[index]
 
        #    index = index-1

        #index = 0
        #while (index < len(arr) - 1):
        #    least = arr[index]
        #    if least < K:
        #        second_least = arr[index+1]
        #        del arr[index+1]
        #        del arr[index]
        #        arr.insert(index, least + second_least)
        #        del intervals[index+1]
        #    index = index + 1

        index = 0
        while (index < len(arr) - 1):
            least = arr[index]
            if least == 0 or least + arr[index+1] <= K:
                second_least = arr[index+1]
                del arr[index+1]
                del arr[index]
                arr.insert(index, least + second_least)
                del intervals[index+1]
                index = index - 1
            index = index + 1

        #index = len(arr) - 1
        #while (index > 0):
        #    least = arr[index]
        #    if least == 0 or least + arr[index-1] <= K:
        #        second_least = arr[index-1]
        #        del arr[index]
        #        del arr[index-1]
        #        arr.insert(index-1, least + second_least)

        #        del intervals[index]
 
        #    index = index-1        

        return arr, intervals
    
    @staticmethod
    def getMinMax(dataTrain, min = sys.maxsize, max = -sys.maxsize - 1):
        for i in dataTrain:
            if i > max:
                max = i
            if i < min:
                min = i

        return min, max

    @staticmethod
    def plotBar(x, data, yLabel='', width = 0.35):
        if not data == None:
            fig, ax = plt.subplots(figsize=(40,5))
            ax.bar(x, height=data)
            ax.set_ylabel(yLabel)
            ax.set_xticks(x)
            ax.legend()

            return data
        
    @staticmethod
    def plotData(x, data1, yLabel=''):
        if not data1 == None:
        #    hist, bins = np.histogram(data1, bins=x)
        #    fig, ax = plt.subplots(figsize=(40,5))
        #    width=[bins[i] - bins[i-1] for i in range(1, len(bins))]
        #    ax.bar([bins[i] + (width[i] / 2) for i in range(len(bins) - 1)], hist.astype(np.float32) / hist.sum(), width=width)
        #    ax.set_ylabel(yLabel)
        #    ax.set_xticks(x)
        #    ax.legend()

            fig, ax = plt.subplots(figsize=(40,5))
            n, x1, _ = ax.hist(data1, bins=x, density = True)

            bin_centers = 0.5*(x1[1:]+x1[:-1])
            ax.plot(bin_centers, n)

            ax.set_ylabel(yLabel)
            ax.set_xticks(x)
            ax.legend()

            return list(n)

    @staticmethod
    def minOperationsByDividing(data, intervals):
        isContinue = True
        while isContinue == True:
            res = Plotter.countInIntervals(data, intervals)
            s = sum(res) / 10 * 3
            indexDividing = []
            for i in range(len(res)):
                if res[i] > s:
                    indexDividing.append(i)

            for i in range(len(indexDividing) - 1, -1, -1):
                i1 = intervals[indexDividing[i]]
                i2 = intervals[indexDividing[i]+1]
                if i2 - i1 < 0.01:
                    indexDividing.pop(i)
                else:
                    intervals.insert(indexDividing[i] + 1, (i2+i1)/2)

            isContinue = False if len(indexDividing) == 0 else True


    @staticmethod
    def countInIntervals(data, intervals):
        res = [0] * (len(intervals) - 1)
        for i in data:
            for j in range(len(intervals)-1):
                if i >= intervals[j] and i <= intervals[j+1]:
                    res[j] = res[j] + 1
                    break

        return res