#import tensorflow as tf
#from tensorflow import keras
#from keras.models import Model
import numpy as np
from Normalizer.MinMaxNormalizer import *
import logging
import json
from Levy import Levy
from random import seed
from random import random
from Locations.LocationsCalculator import LocationsCalculator
import time
from CharacteristicCalculators.Plotter import Plotter
from PathPoint import PathPoint, CentralPoint
from multiprocessing import Pool
import time
from functools import partial
import os

class Network(object):
    model = None
    normalizer = MinMaxNormalizer()
    window = None

    timeModel = None

    layers = []
    locationsCount = 0
    testForGenerate = []
    totalXForCheck = []

    stopModel = None

    def init(self, window, featuresCount, locationsCount, histCount, stopWindow):
        self.window = window
        self.stopWindow = stopWindow
        self.initNetwork(window, featuresCount, locationsCount, histCount, stopWindow)
        self.locationsCount = locationsCount
        seed(round(time.time() * 1000))

    def glueArrays(self, array):
        x = []
        for i in range(0, len(array)):
            x = x + array[i]
        return x

    def train(self, data, trainPercent, minTime, maxTime, minPauseTime, maxPauseTime, stopTrainData, distancesInTrainLocations, rawData, trainPoints, levyCoeff):
        totalTrainX = []
        totalTrainY = []
        totalTestX = []
        totalTestY = []

        totalTrainXParameters = []
        totalTrainYParameters = []
        totalTestXParameters = []
        totalTestYParameters = []

        trainXWithoutGlue = []
        trainParamWithoutGlue = []

        rawXParameters = None

        betweenLocationsX = []
        betweenLocationsY = []

        self.totalTestX = []
        self.totalTestY = []
        self.totalTestParamsX = []
        self.totalTestParamsY = []

        #self.normalizer.Restore(None)

        for arr in data:
            if len(arr) < self.window:
                trainXWithoutGlue.append([])
                trainParamWithoutGlue.append([])
                continue
            train_size = int(len(arr) * (trainPercent / 100))
            test_size = len(arr) - train_size

            x = []
            a = [0] * self.locationsCount

            wg = []
            wgt = []

            a[arr[0].departure.Number] = 1
            x.append(a)
            t = []

            wg.append(a.copy())

            for i in range(len(arr)):
                a1 = [0] * self.locationsCount
                a1[arr[i].destination.Number] = 1
                x.append(a1)
                wg.append(a1.copy())

                a = [Levy.levyCalculate(arr[i].time, minTime, maxTime/levyCoeff), Levy.levyCalculate(arr[i].pauseTime, minPauseTime, maxPauseTime / levyCoeff)]
                wgt.append(a.copy())
                t.append(a)

            #train, test = x[0:train_size], x[train_size:len(x)]

            trainX, trainY = self.create_dataset(x, self.window)
            #testX, testY = self.create_dataset(test, self.window)

            trainXWithoutGlue.append(wg)
            trainParamWithoutGlue.append(wgt)

            #seq = json.dumps(x)
            #seq = json.dumps(t)

            twentyPercent = int(len(trainX) / 100 * 20)

            self.totalTestX.append(trainX[-twentyPercent:]) 
            self.totalTestY.append(trainY[-twentyPercent:]) 
            trainX = trainX[0:len(trainX)-twentyPercent]
            trainY = trainY[0:len(trainY)-twentyPercent]

            for i in range(0, len(trainX)):
                trainX[i] = self.glueArrays(trainX[i])

            #for i in range(0, len(testX)):
            #    testX[i] = self.glueArrays(testX[i])

            totalTrainX = totalTrainX + trainX
            #totalTestX = totalTestX + testX
            totalTrainY = totalTrainY + trainY
            #totalTestY = totalTestY + testY

            trainXParameters, trainYParameters = self.create_dataset(t, self.window - 1)
            #testXParameters, testYParameters = self.create_dataset(t[train_size:len(t)], self.window)

            twentyPercent = int(len(trainXParameters) / 100 * 20)

            self.totalTestParamsX.append(trainXParameters[-twentyPercent:]) 
            self.totalTestParamsY.append(trainYParameters[-twentyPercent:]) 
            trainXParameters = trainXParameters[0:len(trainXParameters)-twentyPercent]
            trainYParameters = trainYParameters[0:len(trainYParameters)-twentyPercent]

            for i in range(0, len(trainX)):
                trainXParameters[i] = self.glueArrays(trainXParameters[i]) + trainX[i].copy()

            #for i in range(0, len(testXParameters)):
            #    testXParameters[i] = self.glueArrays(testXParameters[i])

            totalTrainXParameters = totalTrainXParameters + trainXParameters
            #totalTestXParameters = totalTestXParameters + testXParameters
            totalTrainYParameters = totalTrainYParameters + trainYParameters
            #totalTestYParameters = totalTestYParameters + testYParameters

        for i in range(len(self.totalTestX)):
            result = self.totalTestY[i]
            timeResult = self.totalTestParamsY[i]
            firstPoints = []
            for j in range(len(result)):
                firstPoints.append(trainPoints[i][j].destination)

            with open('lastTestX' + str(i) + '.txt', 'w+') as f:
                    json.dump({"Locations": result, "Time": np.array(timeResult).tolist(), "Points": firstPoints}, f, default=CentralPoint.serialize)
            
        self.fit(self.model, np.array(totalTrainX), np.array(totalTrainY), validation_data=(np.array(totalTestX), np.array(totalTestY)), batchSize=2, epochs=60)
        
        self.fit(self.timeModel, np.array(totalTrainXParameters), np.array(totalTrainYParameters), batchSize=2, epochs=60)

        stopData = []
        stopDataY = []

        for i in range(len(data)):
            if len(data[i]) < self.window:
                continue
            res = self.glueArrays(trainXWithoutGlue[i][-self.stopWindow:])

            d, _ = Plotter.tracesTime([[[], [x]] for x in trainParamWithoutGlue[i]], minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, False)
            
            res.append(sum(d) / Plotter.maxTraceTime)

            d, _ = Plotter.calculateTracesLength([distancesInTrainLocations[i]], False)
            count = Plotter.countInIntervals(d, Plotter.trainIntervals.tracesLength)
            s = sum(count)
            if not s == 0:
                count = [c1 / s for c1 in count]

            res = res + list(count)

            d, _ = Plotter.calculatePauseTimes([[[], [x]] for x in trainParamWithoutGlue[i]], minPauseTime, maxPauseTime, levyCoeff, False)
            count = Plotter.countInIntervals(d, Plotter.trainIntervals.pauseTimes)
            s = sum(count)
            if not s == 0:
                count = [c1 / s for c1 in count]

            res = res + count

            stopData.append(res)
            stopDataY.append(1)

            for c in range(self.stopWindow, len(trainXWithoutGlue[i]), 1):
                sx = trainXWithoutGlue[i][c-self.stopWindow:c]
                sx = self.glueArrays(sx)
                sy = 0
                d, _ = Plotter.tracesTime([[[], [x]] for x in trainParamWithoutGlue[i][:c]], minTime, maxTime, minPauseTime, maxPauseTime, levyCoeff, False)
                sx.append(sum(d) / Plotter.maxTraceTime)

                length = [0] * self.locationsCount
                
                currLocs = trainXWithoutGlue[i][:c]

                try:
                    for locIndex in range(len(currLocs) - 1):
                        if(currLocs[locIndex].index(1) == currLocs[locIndex+1].index(1)):
                            length[currLocs[locIndex].index(1)] += PathPoint.distanceInMetersBetweenEarthCoordinates(trainPoints[i][locIndex].departurePoint.latitude, trainPoints[i][locIndex].departurePoint.longitude, trainPoints[i][locIndex].destination.latitude, trainPoints[i][locIndex].destination.longitude)
                except:
                    exc = 0
                d, _ = Plotter.calculateTracesLength([length], False)
                count = Plotter.countInIntervals(d, Plotter.trainIntervals.tracesLength)
                s = sum(count)
                if not s == 0:
                    count = [c1 / s for c1 in count]

                sx = sx + count

                d, _ = Plotter.calculatePauseTimes([[[], [x]] for x in trainParamWithoutGlue[i][:c]], minPauseTime, maxPauseTime, levyCoeff, False)
                count = Plotter.countInIntervals(d, Plotter.trainIntervals.pauseTimes)
                s = sum(count)
                if not s == 0:
                    count = [c1 / s for c1 in count]

                sx = sx + count

                stopData.append(sx)
                stopDataY.append(0)

        self.fit(self.stopModel, np.array(stopData), np.array(stopDataY), batchSize=3, epochs=60)

        totalInside = 0
        totalOutside = 0

        for i in range(len(data)):
            if len(data[i]) < self.window:
                continue
            for j in range(len(data[i]) - self.window):
                res = self.glueArrays(trainXWithoutGlue[i][j: j + self.window])
                currLoc = trainXWithoutGlue[i][j + self.window - 1].index(1)
                nextLoc = trainXWithoutGlue[i][j + self.window].index(1)
                betweenLocationsX.append(res + trainParamWithoutGlue[i][j + self.window - 1])

                if not currLoc == nextLoc:
                    totalOutside += 1
                    betweenLocationsY.append([0, 1])
                else:
                    totalInside += 1
                    betweenLocationsY.append([1, 0])

        print('totalInside: ' + str(totalInside) + ' totalOutside: ' + str(totalOutside))

        self.fit(self.betweenLocationsModel, np.array(betweenLocationsX), np.array(betweenLocationsY), batchSize=2, epochs=60)

    def normalize(self, data):
        return self.normalizer.Normalize(data)
        
    def addLayer(self, layer):
        self.model.add(layer)
        self.layers.append(layer)

    def initNetwork(self, window, featuresCount, locationsCount, histCount, stopWindow):
        import tensorflow as tf
        from tensorflow import keras
        from keras.models import Model

        self.layers = []
        self.model = keras.models.Sequential()
        self.addLayer(tf.keras.layers.Input(shape=(window * locationsCount)))
        self.addLayer(tf.keras.layers.Dense(80))
        self.addLayer(tf.keras.layers.Dense(locationsCount, activation=tf.keras.activations.softmax))

        self.model.compile(optimizer='adam', loss='categorical_crossentropy')
        #self.model.build()

        self.timeModel = keras.models.Sequential()
        self.timeModel.add(tf.keras.layers.Input(shape=(window * locationsCount + (window - 1) * 2)))
        self.timeModel.add(tf.keras.layers.Dense(80))
        self.timeModel.add(tf.keras.layers.Dense(2))

        self.timeModel.compile(optimizer='adam', loss='mse')
        #self.timeModel.build()

        self.stopModel = keras.models.Sequential()
        self.stopModel.add(tf.keras.layers.Input(shape=(histCount + stopWindow * locationsCount)))
        self.stopModel.add(tf.keras.layers.Dense(40))
        self.stopModel.add(tf.keras.layers.Dense(1))

        self.stopModel.compile(optimizer='adam', loss='mse')

        self.betweenLocationsModel = keras.models.Sequential()
        self.betweenLocationsModel.add(tf.keras.layers.Input(shape=(window * locationsCount + 2)))
        self.betweenLocationsModel.add(tf.keras.layers.Dense(80))
        #self.betweenLocationsModel.add(tf.keras.layers.Dense(20))
        self.betweenLocationsModel.add(tf.keras.layers.Dense(2))

        self.betweenLocationsModel.compile(optimizer='adam', loss='mse')

    def fit(self, model, X, Y, validation_data=None, batchSize=None, epochs=60):
        import tensorflow as tf
        if(model != None):
            #if batchSize == None:
            #    batchSize = len(X)
            with tf.device('/CPU:0'):
                model.fit(X, Y, epochs=epochs, validation_data = validation_data, batch_size = batchSize)

    def generate(self, locations, parameters, countArr, firstPointsArray, minPauseTime, maxPauseTime, levyCoeff, controller):
        totalInside = 0
        totalOutside = 0

        globalResult = []

        betweenLocsRes = []

        #model = Model(inputs=self.model.input, outputs=self.model.layers[-1].input)

        for i in range(len(locations)):
            result = locations[i].copy()
            #result.append(locations[i][len(locations[i])-1])
            timeResult = parameters[i].copy()
            pointsResult = []
            i1 = 0
            startPoints = locations[i].copy()
            timePoints = parameters[i].copy()
            firstPoints = firstPointsArray[i].copy()
            isStop = False

            if(len(timePoints) < self.window - 1):
                print('not enough points')
                continue

            mediumSpeed = 0
            for i in range(len(firstPoints) - 1):
                point = firstPoints[i+1]
                c = firstPoints[i]
                mediumSpeed += PathPoint.distanceInMetersBetweenEarthCoordinates(point.latitude, point.longitude, c.latitude, c.longitude) / Levy.restoreLevy(timeResult[i][0], controller.minTime, controller.maxTime / levyCoeff)
            
            mediumSpeed /= len(timeResult)

            blr = []
            blt = []
            blp = []
            for j in range(len(locations[i]) - 1):
                if(not locations[i][j].index(1) == locations[i][j + 1].index(1)):
                    blr.append(locations[i][j].copy())
                    blr.append(locations[i][j + 1].copy())
                    blt.append(parameters[i][j].copy())
                    blp.append(firstPointsArray[i][j])
                    blp.append(firstPointsArray[i][j+1])

            while(i1 < countArr[i] * 1.5 and not isStop == True):#countArr[i]):
                print(str(i) + ':' + str(i1 + 1) + ' from ' + str(countArr[i]))

                glue = self.glueArrays(startPoints)

                betweenLocations = self.betweenLocationsModel.predict([glue + timePoints[len(timePoints)-1]])
                betweenLocations = list(betweenLocations[0])

                print('Inside: ' + str(betweenLocations[0]) + ' Outside: ' + str(betweenLocations[1]))

                betweenLocations = betweenLocations.index(max(betweenLocations))

                outside = False

                if betweenLocations == 1:
                    res = self.model.predict([glue])

                    res = list(res[0])

                    rand = random()

                    res.pop(startPoints[len(startPoints) - 1].index(1))

                    dictionary = dict(enumerate(res))
                    dictionary = sorted(dictionary.items(), key=lambda x: x[1])
                    selected = -1
                    for k, v in dictionary:
                        if v > rand:
                            if not res.index(max(res)) == k:
                                print('next location is not max')
                            selected = k
                            break
                    if selected == -1:
                        selected = res.index(max(res))

                    totalOutside += 1

                    blr.append(startPoints[len(startPoints) - 1].copy())
                    outside = True
                else:
                    selected = startPoints[len(startPoints) - 1].index(1)
                    count = LocationsCalculator.getLocationPointsCount(selected)
                    if(count < 2):
                        res = self.model.predict([glue])

                        res = list(res[0])

                        rand = random()

                        res.pop(startPoints[len(startPoints) - 1].index(1))

                        dictionary = dict(enumerate(res))
                        dictionary = sorted(dictionary.items(), key=lambda x: x[1])
                        selected = -1
                        for k, v in dictionary:
                            if v > rand:
                                if not res.index(max(res)) == k:
                                    print('next location is not max')
                                selected = k
                                break
                        if selected == -1:
                            selected = res.index(max(res))

                        totalOutside += 1

                        blr.append(startPoints[len(startPoints) - 1].copy())
                        outside = True
                    else:
                        totalInside += 1

                a = [0] * self.locationsCount
                a[selected] = 1

                if(outside == True):
                    point = LocationsCalculator.getNextPointBetweenPointAndLocation(firstPoints[len(firstPoints)-1], selected)

                    firstPoints.append(point)

                    blr.append(a.copy())
                    blp.append(firstPoints[len(firstPoints)-1])
                    blp.append(point)

                res = a

                startPoints.append(res)
                result.append(res)
                startPoints.pop(0)

                glue = self.glueArrays(timePoints) + glue
                res = self.timeModel.predict(np.array([glue]))
                res = list(res[0])
                if res[1] < 0:
                    res[1] = 0
                    print('something strange')
                    print(str(timePoints))
                if res[0] < 0:
                    res[0] = 0
                    print('something very strange')
                    print(str(timePoints))

                if(outside == True):
                    blt.append(res.copy())

                timePoints.append(res)
                timeResult.append(res)
                timePoints.pop(0)

                if(outside == False):
                    point = LocationsCalculator.getNextPointInsideLocation(firstPoints[len(firstPoints)-1], selected, Levy.restoreLevy(res[0], controller.minTime, controller.maxTime / levyCoeff), mediumSpeed)

                    firstPoints.append(point)

                stopEnter = result[-self.stopWindow:]
                stopEnter = self.glueArrays(stopEnter)

                traceTime = 0
                for tr in timeResult:
                    traceTime = traceTime + tr[0] + tr[1]
            
                stopEnter.append(traceTime / Plotter.maxTraceTime)

                length = [0] * self.locationsCount

                for locIndex in range(len(result) - 1):
                    if(result[locIndex].index(1) == result[locIndex+1].index(1)):
                        length[result[locIndex].index(1)] += PathPoint.distanceInMetersBetweenEarthCoordinates(firstPoints[locIndex].latitude, firstPoints[locIndex].longitude, firstPoints[locIndex + 1].latitude, firstPoints[locIndex + 1].longitude)

                d, _ = Plotter.calculateTracesLength([length], False)
                count = Plotter.countInIntervals(d, Plotter.trainIntervals.tracesLength)
                s = sum(count)
                if not s == 0:
                    count = [c / s for c in count]

                stopEnter = stopEnter + count

                d, _ = Plotter.calculatePauseTimes([[[], [x]] for x in timeResult], minPauseTime, maxPauseTime, levyCoeff, False)
                count = Plotter.countInIntervals(d, Plotter.trainIntervals.pauseTimes)
                s = sum(count)
                if not s == 0:
                    count = [c / s for c in count]

                stopEnter = stopEnter + count

                stop = list(self.stopModel.predict(np.array([stopEnter]))[0])[0]

                print('stop: ' + str(stop))

                #if stop > 0.5:
                #    rand = random()
                #    if stop > rand:
                #        isStop = True

                rand = random()
                if stop > rand:
                    isStop = True

                #if stop > 0.5:
                #    rand = random()
                #    if rand <= stop:
                #        break

                i1 = i1 + 1

            globalResult.append([result, timeResult, firstPoints])
            betweenLocsRes.append([blr, blt, blp])

            with open('lastGenerated' + str(i) + '.txt', 'w+') as f:
                json.dump({"Locations": result, "Time": np.array(timeResult).tolist(), "Points": firstPoints}, f, default=CentralPoint.serialize)

            #with open('lastGenerated' + str(i) + '.txt', 'r') as f:
            #    obj = json.load(f, object_hook=CentralPoint.deserialize)
            #    m = obj[0]
            #    m1 = obj[1]
            #    m2 = obj[2]

        #countOfErrors = self.checkGeneration(result)

        print('totalInside: ' + str(totalInside) + ' totalOutside: ' + str(totalOutside))

        return globalResult#betweenLocsRes#

    @staticmethod
    def to_dict(obj):
        if isinstance(obj, CentralPoint) == True:
            return json.dumps(obj.firstPoints, default=CentralPoint.serialize)
        return {
            "Locations": obj.result,
            "Time": obj.timeResult,
            "Points": json.dumps(obj.firstPoints, default=CentralPoint.serialize)
            }

    def checkGeneration(self, generatedArray):
        countOfErrors = 0

        for i in range(len(generatedArray)):
            max_value = max(generatedArray[i])
            max_index = generatedArray[i].index(max_value)
            maxY = max(self.testForGenerate[i])
            maxYIndex = self.testForGenerate[i].index(maxY)
            if(not max_index == maxYIndex):
                countOfErrors = countOfErrors + 1

        return countOfErrors

    def toNpArray(self, list):
        c = np.array().append(np.array().append(np.array(list[0][0])))
        return c

    def serialize(self):
        self.model.save("models/model")
        self.timeModel.save("models/timeModel")
        self.stopModel.save("models/stopModel")
        self.betweenLocationsModel.save("models/betweenLocationsModel")

    def load(self):
        pass
        #from keras.models import load_model

        #self.model = load_model("models/model")
        #self.timeModel = load_model("models/timeModel")
        #self.stopModel = load_model("models/stopModel")
        #self.betweenLocationsModel = load_model("models/betweenLocationsModel")

    def predict(self, X, Y):
        result = []
        for i in range(len(X)):
            res = self.model.predict([X[i]])
            res = self.normalizer.Denormalize(res[0])
            
            y = self.normalizer.Denormalize(Y[i])

            result.append(res)

        return result

    def create_dataset(self, dataset, look_back=1):
        dataX, dataY = [], []
        i = 0
        while (i + look_back < len(dataset)):
        #for i in range(len(dataset) - look_back):
            a = dataset[i:(i + look_back)]
            dataX.append(a)
            dataY.append(dataset[i + look_back])
            i = i + 1
        return dataX, dataY

    def generateProcess(self, controller):
        #start_time = time.time()
        #self.predictData(controller, 1)
        #self.predictData(controller, 1)
        #self.predictData(controller, 1)
        #self.predictData(controller, 1)
        #print("--- %s seconds ---" % (time.time() - start_time))
        countToCalculate = 5000
        allRes = []
        poolProcesses = os.cpu_count()
        start_time = time.time()
        with Pool(processes = poolProcesses) as pool:
            res = pool.map(partial(self.predictData, ([controller, LocationsCalculator.locations, Plotter.maxTraceTime, Plotter.trainIntervals])), range(countToCalculate))
        allRes.append(res)
        print("--- %s seconds ---" % (time.time() - start_time))

    def predictData(self, data, index):
        from keras.models import load_model

        controller = data[0]
        LocationsCalculator.locations = data[1]
        maxTraceTime = data[2]
        trainIntervals = data[3]

        model = load_model("models/model")
        timeModel = load_model("models/timeModel")
        stopModel = load_model("models/stopModel")
        betweenLocationsModel = load_model("models/betweenLocationsModel")

        generatedCount = 0
        isStop = False
        startPoints = [[0] * self.locationsCount, [0] * self.locationsCount, [0] * self.locationsCount, [0] * self.locationsCount, [0] * self.locationsCount]
        startPoints[0][0] = 1
        startPoints[1][1] = 1
        startPoints[2][1] = 1
        startPoints[3][0] = 1
        startPoints[4][0] = 1

        locs = startPoints.copy()

        timePoints = [[0.04270244525723281, 0.0], [0.0, 6.107682048886656e-05], [0.05024291912937793, 0.28987704889569355], [0.39358159311554197, 2.377966898667236e-103]]
        timeResult = timePoints.copy()

        allPoints = [CentralPoint(-141.82781784612698, 517.7097847500308, 0), CentralPoint(-255.15099254362417, 198.23341618557382, 1), CentralPoint(-257.01172031057325, 199.41523615579274, 2), CentralPoint(-139.67705836388706, 492.2189819884441, 3), CentralPoint(-588.8921239628572, -297.25939287414906, 4)]

        traceTime = 0
        for tr in timeResult:
            traceTime = traceTime + tr[0] + tr[1]

        while(generatedCount < 100 and not isStop == True):
            glue = self.glueArrays(startPoints)
            betweenLocations = betweenLocationsModel.predict([glue + timePoints[len(timePoints)-1]])
            betweenLocations = list(betweenLocations[0])
            betweenLocations = betweenLocations.index(max(betweenLocations))

            locRes = model.predict([glue])
            locRes = list(locRes[0])

            if betweenLocations == 1:
                rand = random()

                dictionary = dict(enumerate(locRes))
                dictionary = sorted(dictionary.items(), key=lambda x: x[1])
                selected = -1
                for k, v in dictionary:
                    if v > rand:
                        selected = k
                        break
                if selected == -1:
                    selected = locRes.index(max(locRes))

                point = LocationsCalculator.getNextPointBetweenPointAndLocation(allPoints[len(allPoints)-1], selected)
            else:
                selected = startPoints[len(startPoints) - 1].index(1)
                count = LocationsCalculator.getLocationPointsCount(selected)
                if(count < 2):
                    rand = random()

                    locRes.pop(startPoints[len(startPoints) - 1].index(1))

                    dictionary = dict(enumerate(locRes))
                    dictionary = sorted(dictionary.items(), key=lambda x: x[1])
                    selected = -1
                    for k, v in dictionary:
                        if v > rand:
                            selected = k
                            break
                    if selected == -1:
                        selected = locRes.index(max(locRes))

                    point = LocationsCalculator.getNextPointBetweenPointAndLocation(allPoints[len(allPoints)-1], selected)
                else:
                    point = None

            a = [0] * self.locationsCount
            a[selected] = 1

            glue = self.glueArrays(timePoints) + glue
            res = timeModel.predict(np.array([glue]))
            res = list(res[0])
            if res[1] < 0:
                res[1] = 0
            if res[0] < 0:
                res[0] = 0

            timePoints.append(res)
            timeResult.append(res)
            timePoints.pop(0)

            if(point == None):
                mediumSpeed = 0
                for i in range(len(allPoints) - 1):
                    cp = allPoints[i+1]
                    c = allPoints[i]
                    mediumSpeed += PathPoint.distanceInMetersBetweenEarthCoordinates(cp.latitude, cp.longitude, c.latitude, c.longitude) / Levy.restoreLevy(timeResult[i][0], controller.minTime, controller.maxTime / controller.levyCoeff)
            
                mediumSpeed /= len(timeResult)
                point = LocationsCalculator.getNextPointInsideLocation(allPoints[len(allPoints)-1], selected, Levy.restoreLevy(res[0], controller.minTime, controller.maxTime / controller.levyCoeff), mediumSpeed)

            allPoints.append(point)

            startPoints.append(a)
            locs.append(a)
            startPoints.pop(0)

            stopEnter = locs[-self.stopWindow:]
            stopEnter = self.glueArrays(stopEnter)

            traceTime = traceTime + res[0] + res[1]
            
            stopEnter.append(traceTime / maxTraceTime)

            length = [0] * self.locationsCount

            for locIndex in range(len(locs) - 1):
                if(locs[locIndex].index(1) == locs[locIndex+1].index(1)):
                    length[locs[locIndex].index(1)] += PathPoint.distanceInMetersBetweenEarthCoordinates(allPoints[locIndex].latitude, allPoints[locIndex].longitude, allPoints[locIndex + 1].latitude, allPoints[locIndex + 1].longitude)

            d, _ = Plotter.calculateTracesLength([length], False)
            count = Plotter.countInIntervals(d, trainIntervals.tracesLength)
            s = sum(count)
            if not s == 0:
                count = [c / s for c in count]

            stopEnter = stopEnter + count

            d, _ = Plotter.calculatePauseTimes([[[], [x]] for x in timeResult], controller.minPauseTime, controller.maxPauseTime, controller.levyCoeff, False)
            count = Plotter.countInIntervals(d, trainIntervals.pauseTimes)
            s = sum(count)
            if not s == 0:
                count = [c / s for c in count]

            stopEnter = stopEnter + count

            stop = list(stopModel.predict(np.array([stopEnter], dtype=np.float32))[0])[0]

            rand = random()
            if stop > rand:
                isStop = True
            generatedCount += 1

        return locs