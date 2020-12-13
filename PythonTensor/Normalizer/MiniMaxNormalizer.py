from Normalizer.AbstractNormalizer import AbstractNormalizer

class MiniMaxNormalizer(AbstractNormalizer):
    self.Min = 0
    self.Max = 0

    def FindMinAndMax(self, data):
        for d in data:
            if d < self.Min:
                self.Min = d
            elif d > self.Max:
                self.Max = d

    def FitAndNormalize(self, data):
        FindMinAndMax(data)
        return Normalize(data)

    def Normalize(self, data):
        result = []
        for d in data:
            result.append((d - self.Max) / (self.Max - self.Min))

        return result