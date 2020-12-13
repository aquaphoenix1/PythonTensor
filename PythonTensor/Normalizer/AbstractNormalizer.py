from abc import abstractmethod, ABC

class AbstractNormalizer(ABC):
    @abstractmethod
    def Normalize(self, data):
        pass

    @abstractmethod
    def FitAndNormalize(self, data):
        pass