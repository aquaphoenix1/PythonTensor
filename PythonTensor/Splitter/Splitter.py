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
                f.write(i.departurePoint.toString() + ' ' + i.destination.toString() + ' ' + str(i.time) + '\n')


        return sets

    def converToJumpList(self, sets):
        jumpList = list()
        for i in range(len(sets) - 1):
            time = sets[i+1].getFirstPoint().date - sets[i].getLastPoint().date
            jumpList.append(Jump(sets[i].center, sets[i+1].center, time))

        return jumpList

    def convertCoord(self, coord):
        grad = int(coord)
        g = int(grad / 100)
        m = grad - (g * 100)
        sec = int((coord - grad) * 100)
        return g + m / 60 + sec / 3600