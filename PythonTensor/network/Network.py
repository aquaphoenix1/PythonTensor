import tensorflow as tf
from tensorflow import keras
import numpy

class Network(object):
    model = None

    def test(self, data):
        testPercent = 30
        learnPercent = 100 - testPercent
        onePercent = 100.0 / len(data)
        inputSize = 3

        currentPercent = inputSize * onePercent

        learnX = []
        testX = []
        learnY = []
        testY = []

        #for i in range(len(data) - inputSize):
        #    x = []
        #    for j in range(inputSize):
        #            d = [data[i + j].departurePoint.latitude, data[i + j].departurePoint.longitude, data[i + j].destination.latitude, data[i + j].destination.longitude, data[i + j].time]
        #            x.append(d)
        #    if currentPercent < learnPercent:
        #        learnX.append(x)
        #    else:
        #        testX.append(x)
        #    if currentPercent < learnPercent:
        #        learnY.append([data[i + inputSize].departurePoint.latitude, data[i + inputSize].departurePoint.longitude, data[i + inputSize].destination.latitude, data[i + inputSize].destination.longitude, data[i + inputSize].time])
        #    else:
        #        testY.append([data[i + inputSize].departurePoint.latitude, data[i + inputSize].departurePoint.longitude, data[i + inputSize].destination.latitude, data[i + inputSize].destination.longitude, data[i + inputSize].time])
            
        #    currentPercent = currentPercent + onePercent

        x = []
        for i in range(len(data)):
            x.append([data[i].departurePoint.latitude, data[i].departurePoint.longitude, data[i].destination.latitude, data[i].destination.longitude, data[i].time])

        trainX, trainY = self.create_dataset(x, inputSize)
        #trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))

        self.init(inputSize, 5)
        self.fit(trainX, trainY)
        self.predict(trainX, trainY)

    def init(self, inputSize, featuresCount):
        self.model = keras.models.Sequential()
        self.model.add(tf.keras.layers.LSTM(100, input_shape=(inputSize, featuresCount)))
        self.model.add(tf.keras.layers.Dense(featuresCount))
        self.model.compile(optimizer='adam', loss='mse')

    def fit(self, X, Y, epochs = 80):
        if(self.model != None):
            self.model.fit(X, Y, epochs=epochs)

    def predict(self, X, Y):
        #if(len(X) == 1):
        #    return [self.model.predict(X)]

        result = []
        for x in X:
            result.append(self.model.predict(x))

        return result

    def create_dataset(self, dataset, look_back=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back)]
            dataX.append(a)
            dataY.append(dataset[i + look_back])
        return numpy.array(dataX), numpy.array(dataY)