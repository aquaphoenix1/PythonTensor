from Splitter.AbstractSplitter import AbstractSplitter
from datetime import datetime, date, time
from Point import Point
from Set import Set

class DaySplitter(AbstractSplitter):
    def Split(self, data):
        data = data.split('\n')
        sets = []
        d = []
        index = 0
        setsSize = 0
        firstTime = None
        try:
            for i in data:
                if len(i) == 0:
                    continue
                splitData = i.split(',')
                if firstTime is None:
                    firstTime = self.convertToDate(splitData[0])
                    d.insert(index, Point(firstTime, float(splitData[1]), float(splitData[2]), float(splitData[3]), float(splitData[4]), float(splitData[5])))
                    index = index + 1
                else:
                    date = self.convertToDate(splitData[0])
                    if abs((date - firstTime).days) == 0:
                        d.insert(index, Point(date, float(splitData[1]), float(splitData[2]), float(splitData[3]), float(splitData[4]), float(splitData[5])))
                        index = index + 1
                    else:
                        sets.insert(setsSize, Set(setsSize, d))
                        setsSize = setsSize + 1
                        index = 0
                        d = []
                        firstTime = None
        except Exception as ex:
            print(ex)

        return sets