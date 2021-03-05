from abc import abstractmethod
from datetime import date

class AbstractSplitter(object):
    @abstractmethod
    def split(self, data, fileName):
        pass

    def convertToDate(self, time):
        return date.fromtimestamp(int(time)/1000.0)