import tensorflow as tf
from tensorflow import keras

class Network(object):
    model = None

    def init(self, inputSize, n_features):
        self.model = keras.models.Sequential()
        self.model.add(tf.keras.layers.LSTM(100, activation='relu', return_sequences=True, input_shape=(inputSize, n_features)))
        self.model.add(tf.keras.layers.LSTM(100, activation='relu'))
        self.model.add(tf.keras.layers.Dense(n_features))
        self.model.compile(optimizer='adam', loss='mse')

    def fit(self, X, Y, epochs = 200):
        if(self.model != None):
            model.fit(X, Y, epochs)

    def predict(self, X):
        #if(len(X) == 1):
        #    return [self.model.predict(X)]

        result = []
        for x in X:
            result.append(self.model.predict(x))

        return result