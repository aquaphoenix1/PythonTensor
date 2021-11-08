from Splitter.AbstractSplitter import AbstractSplitter
from datetime import datetime, date, time
from Point import Point
from Set import Set
from PathPoint import *
from Jump import Jump

class Splitter(AbstractSplitter):
    def Split(self, data, fileName):
        data = data.split('\n')
        sets = []

        currentPathPoint = PathPoint()

        try:
            for i in data:
                if not i == "":
                    splitData = i.split(',')
                    lat = self.convertCoord(float(splitData[2]))
                    lon = self.convertCoord(-float(splitData[3]))
                    point = Point(int(splitData[0]), float(splitData[1]), lat, lon, float(splitData[4]), float(splitData[5]))
                    if currentPathPoint.isInsideRadius(point):
                        currentPathPoint.addPoint(point)
                    else:
                        if currentPathPoint.isMoreTime():
                            if not currentPathPoint.getPointsCount() == 1:
                                sets.append(currentPathPoint)
                            currentPathPoint = PathPoint()
                            currentPathPoint.addPoint(point)
                        else:
                            currentPathPoint.addPoint(point)
                            currentPathPoint.recalculate()
        except Exception:
            a = 0
            
        if not currentPathPoint.getPointsCount() == 1:
            sets.append(currentPathPoint)

        jumpList = self.converToJumpList(sets)
        with open(fileName + '.txt', 'w') as f:
            for i in jumpList:
                f.write(i.departurePoint.toString() + ' ' + i.destination.toString() + ' ' + str(i.time) +  ' ' + str(i.pauseTime) + '\n')