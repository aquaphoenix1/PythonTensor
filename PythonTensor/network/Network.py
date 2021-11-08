import tensorflow as tf
from tensorflow import keras
import numpy as np
from Normalizer.MinMaxNormalizer import *
import logging
import json
from Levy import Levy
from random import seed
from random import random
from Locations.LocationsCalculator import LocationsCalculator
import time

class Network(object):
    model = None
    normalizer = MinMaxNormalizer()
    window = None

    timeModel = None

    layers = []
    locationsCount = 0
    testForGenerate = []
    totalXForCheck = []

    def init(self, window, featuresCount, locationsCount):
        self.window = window
        self.initNetwork(window, featuresCount, locationsCount)
        self.locationsCount = locationsCount
        seed(round(time.time() * 1000))

    def glueArrays(self, array):
        x = []
        for i in range(0, len(array)):
            x = x + array[i]
        return x

    def train(self, data, trainPercent, minTime, maxTime, minPauseTime, maxPauseTime):     
        totalTrainX = []
        totalTrainY = []
        totalTestX = []
        totalTestY = []

        totalTrainXParameters = []
        totalTrainYParameters = []
        totalTestXParameters = []
        totalTestYParameters = []

        #self.normalizer.Restore(None)

        for arr in data:
            train_size = int(len(arr) * (trainPercent / 100))
            test_size = len(arr) - train_size

            x = []
            a = []
            for i in range(self.locationsCount):
                a.append(0)
            a[arr[0].departure.Number] = 1
            x.append(a)
            t = []

            try:
                for i in range(len(arr)):
                    a = []
                    for k in range(self.locationsCount):
                        a.append(0)
                    a[arr[i].destination.Number] = 1
                    x.append(a)
                    a = [Levy.levyCalculate(arr[i].time, minTime, maxTime/4), Levy.levyCalculate(arr[i].pauseTime, minPauseTime, maxPauseTime / 4)]
                    t.append(a)
            except:
                logging.error('error processed')

            train, test = x[0:train_size], x[train_size:len(x)]

            trainX, trainY = self.create_dataset(train, self.window)
            testX, testY = self.create_dataset(test, self.window)

            seq = json.dumps(x)
            seq = json.dumps(t)

            for i in range(0, len(trainX)):
                trainX[i] = self.glueArrays(trainX[i])

            for i in range(0, len(testX)):
                testX[i] = self.glueArrays(testX[i])

            totalTrainX = totalTrainX + trainX
            totalTestX = totalTestX + testX
            totalTrainY = totalTrainY + trainY
            totalTestY = totalTestY + testY

            trainXParameters, trainYParameters = self.create_dataset(t[0:len(t)], self.window)
            testXParameters, testYParameters = self.create_dataset(t[train_size:len(t)], self.window)

            for i in range(0, len(trainXParameters)):
                trainXParameters[i] = self.glueArrays(trainXParameters[i])

            for i in range(0, len(testXParameters)):
                testXParameters[i] = self.glueArrays(testXParameters[i])

            totalTrainXParameters = totalTrainXParameters + trainXParameters
            totalTestXParameters = totalTestXParameters + testXParameters
            totalTrainYParameters = totalTrainYParameters + trainYParameters
            totalTestYParameters = totalTestYParameters + testYParameters


        self.testForGenerate = totalTrainY + totalTestY
        self.totalXForCheck = totalTrainX + totalTestX
            
        self.fit(self.model, np.array(totalTrainX), np.array(totalTrainY), validation_data=(np.array(totalTestX), np.array(totalTestY)), batchSize=2, epochs=150)

        self.fit(self.timeModel, np.array(totalTrainXParameters), np.array(totalTrainYParameters), batchSize=2)

    def normalize(self, data):
        return self.normalizer.Normalize(data)
        
    def addLayer(self, layer):
        self.model.add(layer)
        self.layers.append(layer)

    def initNetwork(self, inputSize, featuresCount, locationsCount):
        self.layers = []
        self.model = keras.models.Sequential()
        self.addLayer(tf.keras.layers.Input(shape=(inputSize * locationsCount)))
        self.addLayer(tf.keras.layers.Dense(45))
        #self.addLayer(tf.keras.layers.Dense(20))
        #self.addLayer(tf.keras.layers.LSTM(30))
        self.addLayer(tf.keras.layers.Dense(locationsCount, activation=tf.keras.activations.softmax))

        self.model.compile(optimizer='adam', loss='mse')
        #self.model.build()

        self.timeModel = keras.models.Sequential()
        #self.timeModel.add(tf.keras.layers.LSTM(20, input_shape=(1, 6)))
        self.timeModel.add(tf.keras.layers.Input(shape=(inputSize * 2)))
        self.timeModel.add(tf.keras.layers.Dense(20))
        self.timeModel.add(tf.keras.layers.Dense(20))
        #self.timeModel.add(tf.keras.layers.Dropout(0.1))
        #self.timeModel.add(tf.keras.layers.LSTM(20))
        self.timeModel.add(tf.keras.layers.Dense(2))

        self.timeModel.compile(optimizer='adam', loss='mse')
        #self.timeModel.build()

    def fit(self, model, X, Y, validation_data=None, batchSize=None, epochs=100):
        if(model != None):
            #if batchSize == None:
            #    batchSize = len(X)
            model.fit(X, Y, epochs=epochs, validation_data = validation_data, batch_size = batchSize)

    def generate(self, locations, parameters, countArr, firstPointsArray):
        globalResult = []

        for i in range(len(locations)):
            result = locations[i].copy()
            #result.append(locations[i][len(locations[i])-1])
            timeResult = parameters[i].copy()
            pointsResult = []
            i1 = 0
            startPoints = locations[i].copy()
            timePoints = parameters[i].copy()
            firstPoints = firstPointsArray[i].copy()

            while(i1 < countArr[i]):
                print(str(i) + ':' + str(i1 + 1) + ' from ' + str(countArr[i]))
                glue = self.glueArrays(startPoints)
                res = self.model.predict([glue])

                res = list(res[0])
                a = []
                for k in range(self.locationsCount):
                    a.append(0)
                selected = -1
                while selected == -1:
                    for k in range(self.locationsCount):
                        rand = random()
                        if rand <= res[k]:
                            selected = k
                            break

                #selected = res.index(max(res))

                a[selected] = 1

                point = LocationsCalculator.getNextPointBetweenPointAndLocation(firstPoints[len(firstPoints)-1], selected)

                firstPoints.append(point)

                res = a

                startPoints.append(res)
                result.append(res)
                startPoints.pop(0)

                glue = self.glueArrays(timePoints)
                res = self.timeModel.predict(np.array([glue]))
                res = list(res[0])
                if res[1] < 0:
                    res[1] = 0
                    print('something strange')
                    print(str(timePoints))
                timePoints.append(res)
                timeResult.append(res)
                timePoints.pop(0)

                i1 = i1 + 1

            timeResult.pop()
            globalResult.append([result, timeResult, firstPoints])

        #countOfErrors = self.checkGeneration(result)
        return globalResult

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