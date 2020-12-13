from Splitter.AbstractSplitter import AbstractSplitter
from datetime import datetime, date, time
from Point import Point
from Set import Set
from PathPoint import PathPoint

class Splitter(AbstractSplitter):
    def Split(self, data):
        data = data.split('\n')
        sets = []
        #d = []
        #index = 0
        #setsSize = 0
        #firstTime = None
        #try:
        #    for i in data:
        #        if len(i) == 0:
        #            continue
        #        splitData = i.split(',')
        #        if firstTime is None:
        #            firstTime = self.convertToDate(splitData[0])
        #            d.insert(index, Point(int(splitData[0]),
        #            float(splitData[1]), float(splitData[2]),
        #            float(splitData[3]), float(splitData[4]),
        #            float(splitData[5])))
        #            index = index + 1
        #        else:
        #            date = self.convertToDate(splitData[0])
        #            if abs((date - firstTime).days) == 0:
        #                d.insert(index, Point(int(splitData[0]),
        #                float(splitData[1]), float(splitData[2]),
        #                float(splitData[3]), float(splitData[4]),
        #                float(splitData[5])))
        #                index = index + 1
        #            else:
        #                sets.insert(setsSize, Set(setsSize, d))
        #                setsSize = setsSize + 1
        #                index = 0
        #                d = []
        #                firstTime = None
        #except Exception as ex:
        #    print(ex)

        currentPathPoint = PathPoint()

        try:
            for i in data:
                if not i == "":
                    splitData = i.split(',')
                    point = Point(int(splitData[0]), float(splitData[1]), float(splitData[2]), float(splitData[3]), float(splitData[4]), float(splitData[5]))
                    if currentPathPoint.isInsideRadius(point):
                        currentPathPoint.addPoint(point)
                    else:
                        if currentPathPoint.isMoreTime():
                            sets.append(currentPathPoint)
                            currentPathPoint = PathPoint()
                            currentPathPoint.addPoint(point)
                        else:
                            currentPathPoint.addPoint(point)
                            currentPathPoint.recalculate()
        except Exception:
            a = 0
        
        sets.append(currentPathPoint)

        return sets