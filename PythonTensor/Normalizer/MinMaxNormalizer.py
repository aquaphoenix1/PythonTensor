from Normalizer.AbstractNormalizer import AbstractNormalizer
import numpy as np

class MinMaxNormalizer(AbstractNormalizer):
    Min = None
    Max = None

    def FindMinAndMax(self, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] < self.Min[j]:
                    self.Min[j] = data[i][j]
                elif data[i][j] > self.Max[j]:
                    self.Max[j] = data[i][j]

    def FitAndNormalize(self, data):
        self.Fit(data)
        
        return self.Normalize(data)

    def Restore(self, data):
        if(data == None):
            self.Min = None
            self.Max = None
        else:
            for i in range(len(data)):
                for j in range(len(data[i])):
                    self.Min = [data[i][j]] * len(data[0])
                    self.Max = [data[i][j]] * len(data[0])

    def Fit(self, data):
        if(self.Min == None or self.Max == None):
            self.Restore(data)

        self.FindMinAndMax(data)

    def Normalize(self, data):
        result = []
        for i in range(len(data)):
            result.append([])
            for j in range(len(data[i])):
                if(isinstance(data[i][j], np.int32) or isinstance(data[i][j], float)):
                    result[i].append((data[i][j] - self.Min[j]) / (self.Max[j] - self.Min[j]))
                else:
                    result[i].append([])
                    for k in range(len(data[i][j])):
                        result[i][j].append((data[i][j][k] - self.Min[k]) / (self.Max[k] - self.Min[k]))

        return result

    def Denormalize(self, data):
        result = []
        for i in range(len(data)):
            result.append(data[i] * (self.Max[i] - self.Min[i]) + self.Min[i])

        return result