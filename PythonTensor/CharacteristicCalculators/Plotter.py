import matplotlib.pyplot as plt
import numpy as np
from CharacteristicCalculators.Controller import Controller
import sys
from PathPoint import PathPoint

class Plotter(object):
    intervalsCount = 20
    minInInterval = 5

    @staticmethod
    def plot(train, data, distancesInLocation, trainPoints, locationsCount):
        #trained, predicted, it, ip = Plotter.calculateTracesLength(distancesInLocation, data)
        #Plotter.plotData(it, trained, 'Длины трасс в локациях при обучении')
        #Plotter.plotData(ip, predicted, 'Длины трасс в локациях при прогнозировании')

        #trained, predicted, it, ip = Plotter.tracesTime(train, data)
        #Plotter.plotData(it, trained, 'Время прохождения трасс при обучении')
        #Plotter.plotData(ip, predicted, 'Время прохождения трасс при прогнозировании')

        #trained, predicted, it, ip = Plotter.calculateJumpLength(trainPoints, data)
        #Plotter.plotData(it, trained, 'Длины прыжков между локациями при обучении')
        #Plotter.plotData(ip, predicted, 'Длины прыжков между локациями при прогнозировании')

        #trained, predicted, it, ip = Plotter.calculatePauseTimes(train, data)
        #Plotter.plotData(it, trained, 'Время пауз при обучении')
        #Plotter.plotData(ip, predicted, 'Время пауз при прогнозировании')

        #trained, predicted, it, ip = Plotter.calculateLocationsCount(train, data, locationsCount)
        #Plotter.plotBar(it, trained, 'Количество посещений локаций при обучении')
        #Plotter.plotBar(ip, predicted, 'Количество посещений локаций при прогнозировании')

        trained, predicted, it, ip = Plotter.calculateDifferentLocationsCount(train, data, locationsCount)
        Plotter.plotData(it, trained, 'Количество посещений различных локаций при обучении')
        Plotter.plotData(ip, predicted, 'Количество посещений различных локаций при прогнозировании')

        return
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
    def calculateDifferentLocationsCount(train, data, locationsCount):
        trainResult = []
        predictedResult = []
        
        for i in train:
            arr = [0] * locationsCount
            for j in i[0]:
                arr[j.index(1)] = 1
            trainResult.append(arr)

        trainResult = list(np.asarray(trainResult).sum(axis=1))

        predictedTimes = []

        maxVal = max(np.max(trainResult), np.max(predictedTimes, initial=-sys.maxsize - 1))
        minVal = min(np.min(trainResult), np.min(predictedTimes, initial=sys.maxsize))

        count = max(Plotter.intervalsCount, len(trainResult))

        intervals = Plotter.getIntervals(minVal, maxVal, count)

        resultTrained = []
        resultPredicted = []
        for i in range(count):
            resultTrained.append(0)
            resultPredicted.append(0)

        try:
            for i in trainResult:
                for k in range(len(intervals) - 1):
                        if i >= intervals[k] and i <= intervals[k+1]:
                            resultTrained[k] = resultTrained[k]+1
                            break
        except:
            a = 0

        a, indexesTrained = Plotter.minOperations(resultTrained, Plotter.minInInterval, intervals.copy())
        #_, indexesPredicted = Plotter.minOperations(resultPredicted, Plotter.minInInterval, intervals.copy())
        indexesPredicted = []
        return trainResult, predictedResult if not len(data) == 0 else None, indexesTrained, indexesPredicted ##########


    @staticmethod
    def getIntervals(min, max, count):
        intervals = [min]
        step = (max-min)/count
        for i in range(count-1):
            intervals.append(intervals[len(intervals)-1] + step)
        intervals.append(max)
        return intervals

    @staticmethod
    def tracesTime(train, data):
        trainTimes = []
        predictedTimes = []
        for i in train:
            time = 0
            for j in i[1]:
                time = time + j[0] + j[1]

            trainTimes.append(time)

        for i in data:
            time = 0
            for j in i[1]:
                time = time + j[0] + j[1]

            predictedTimes.append(time)

        maxVal = max(np.max(trainTimes), np.max(predictedTimes, initial=-sys.maxsize - 1))
        minVal = min(np.min(trainTimes), np.min(predictedTimes, initial=sys.maxsize))

        intervals = Plotter.getIntervals(minVal, maxVal, Plotter.intervalsCount)

        resultTrained = []
        resultPredicted = []
        for i in range(Plotter.intervalsCount):
            resultTrained.append(0)
            resultPredicted.append(0)

        for i in trainTimes:
            for k in range(len(intervals) - 1):
                    if i >= intervals[k] and i <= intervals[k+1]:
                        resultTrained[k] = resultTrained[k]+1
                        break

        for i in predictedTimes:
            for k in range(len(intervals) - 1):
                    if i >= intervals[k] and i <= intervals[k+1]:
                        resultPredicted[k] = resultPredicted[k]+1
                        break

        _, indexesTrained = Plotter.minOperations(resultTrained, Plotter.minInInterval, intervals.copy())
        _, indexesPredicted = Plotter.minOperations(resultPredicted, Plotter.minInInterval, intervals.copy())

        return trainTimes, predictedTimes if not len(data) == 0 else None, indexesTrained, indexesPredicted

    @staticmethod
    def calculateLocationsCount(train, data, locationsCount):
        resTrained = [0] * locationsCount
        resPredicted = [0] * locationsCount

        for i in train:
            for j in i[0]:
                resTrained[j.index(1)] = resTrained[j.index(1)] + 1

        for i in data:
            for j in i[0]:
                resPredicted[j.index(1)] = resPredicted[j.index(1)] + 1

        return resTrained, resPredicted if not len(data) == 0 else None, np.arange(locationsCount), np.arange(locationsCount)

    @staticmethod
    def calculatePauseTimes(train, data):
        allPausesTrained = []
        allPausesPredicted = []
        maxVal = -sys.maxsize - 1
        minVal = sys.maxsize
        for i in train:
            pausesRows = [row[1] for row in i[1]]
            maxVal = max(maxVal, np.max(pausesRows))
            minVal = min(minVal, np.min(pausesRows))
            allPausesTrained = allPausesTrained + pausesRows

        for i in data:
            pausesRows = [row[1] for row in i[1]]
            maxVal = max(maxVal, np.max(pausesRows))
            minVal = min(minVal, np.min(pausesRows))
            allPausesPredicted = allPausesPredicted + pausesRows

        intervals = Plotter.getIntervals(minVal, maxVal, Plotter.intervalsCount)
        resultTrained = []
        resultPredicted = []
        for i in range(Plotter.intervalsCount):
            resultTrained.append(0)
            resultPredicted.append(0)

        for i in allPausesTrained:
            for k in range(len(intervals) - 1):
                if i >= intervals[k] and i <= intervals[k+1]:
                    resultTrained[k] = resultTrained[k]+1
                    break

        for i in allPausesPredicted:
            for k in range(len(intervals) - 1):
                if i >= intervals[k] and i <= intervals[k+1]:
                    resultPredicted[k] = resultPredicted[k]+1
                    break

        _, indexesTrained = Plotter.minOperations(resultTrained, Plotter.minInInterval, intervals.copy())
        _, indexesPredicted = Plotter.minOperations(resultPredicted, Plotter.minInInterval, intervals.copy())

        return allPausesTrained, allPausesPredicted if not len(data) == 0 else None, indexesTrained, indexesPredicted
        
    @staticmethod
    def calculateJumpLength(distancesInTrainLocation, data):
        distancesTrained = []
        distancesPredicted = []

        for i in distancesInTrainLocation:
            for k in i:
                distancesTrained.append(PathPoint.distanceInMetersBetweenEarthCoordinates(k.departurePoint.latitude, k.departurePoint.longitude, k.destination.latitude, k.destination.longitude))

        for i in data:
            for k in range(len(i[2])-1):
                if not np.argmax(i[0][k]) == np.argmax(i[0][k+1]):
                    firstPoint = i[2][k]
                    secondPoint = i[2][k+1]
                    distancesPredicted.append(PathPoint.distanceInMetersBetweenEarthCoordinates(firstPoint.latitude, firstPoint.longitude, secondPoint.latitude, secondPoint.longitude))

        maxVal = max(np.max(distancesTrained), np.max(distancesPredicted, initial=-sys.maxsize - 1))
        minVal = min(np.min(distancesTrained), np.min(distancesPredicted, initial=sys.maxsize))

        intervals = Plotter.getIntervals(minVal, maxVal, Plotter.intervalsCount)

        resultTrained = []
        resultPredicted = []
        for i in range(Plotter.intervalsCount):
            resultTrained.append(0)
            resultPredicted.append(0)

        for i in distancesTrained:
            for k in range(len(intervals) - 1):
                if i >= intervals[k] and i <= intervals[k+1]:
                    resultTrained[k] = resultTrained[k]+1
                    break

        for i in distancesPredicted:
            for k in range(len(intervals) - 1):
                if i >= intervals[k] and i <= intervals[k+1]:
                    resultPredicted[k] = resultPredicted[k]+1
                    break

        _, indexesTrained = Plotter.minOperations(resultTrained, Plotter.minInInterval, intervals.copy())
        _, indexesPredicted = Plotter.minOperations(resultPredicted, Plotter.minInInterval, intervals.copy())

        return distancesTrained, distancesPredicted if not len(data) == 0 else None, indexesTrained, indexesPredicted

    @staticmethod
    def calculateTracesLength(distancesInTrainLocation, data):
        distancesPredicted = []
        for k in data:
            el = k[0]
            res = [0] * len(el[0])

            for i in range(len(el) - 1):
                if np.argmax(el[i]) == np.argmax(el[i+1]):
                    res[np.argmax(el[i])] = res[np.argmax(el[i])] + PathPoint.distanceInMetersBetweenEarthCoordinates(k[2][i].latitude, k[2][i].longitude, k[2][i+1].latitude, k[2][i+1].longitude)
            distancesPredicted.append(res)

        min = sys.maxsize
        max = -sys.maxsize - 1

        for i in distancesPredicted:
            min, max = Plotter.getMinMax(i, min, max)
        for i in distancesInTrainLocation:
            min, max = Plotter.getMinMax(i, min, max)

        intervals = Plotter.getIntervals(min, max, Plotter.intervalsCount)
        resultTrained = []
        resultPredicted = []
        step = (max-min)/Plotter.intervalsCount
        for i in range(Plotter.intervalsCount):
            resultTrained.append(0)
            resultPredicted.append(0)

        for i in distancesInTrainLocation:
            i = [k for k in i if k != 0]
            for j in range(len(i)):
                for k in range(len(intervals) - 1):
                    if i[j] >= intervals[k] and i[j] <= intervals[k+1]:
                        resultTrained[k] = resultTrained[k]+1
                        break

        for i in distancesPredicted:
            i = [k for k in i if k != 0]
            for j in range(len(i)):
                for k in range(len(intervals) - 1):
                    if i[j] >= intervals[k] and i[j] <= intervals[k+1]:
                        resultPredicted[k] = resultPredicted[k]+1
                        break

        _, intervalsTrained = Plotter.minOperations(resultTrained, Plotter.minInInterval, intervals.copy())
        _, intervalsPredicted = Plotter.minOperations(resultPredicted, Plotter.minInInterval, intervals.copy())

        resultTrained = []
        for i in distancesInTrainLocation:
            resultTrained = resultTrained + i

        resultTrained = [i for i in resultTrained if i != 0]

        resultPredicted = []
        for i in distancesPredicted:
            resultPredicted = resultPredicted + i

        resultPredicted = [i for i in resultPredicted if i != 0]

        return resultTrained, resultPredicted if not len(data) == 0 else None, intervalsTrained, intervalsPredicted

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
        
    @staticmethod
    def plotData(x, data1, yLabel=''):
        if not data1 == None:
            fig, ax = plt.subplots(figsize=(40,5))
            ax.hist(data1, bins=x)
            ax.set_ylabel(yLabel)
            ax.set_xticks(x)
            ax.legend()
        #ax.bar(x, height=data1, label='trained')
        #if not data2==None:
        #    ax.bar(np.arange(len(data2))+width/2, data2, width, label='predicted')
        #ax.set_ylabel(yLabel)
        #ax.set_xticks(x)
        #ax.legend()