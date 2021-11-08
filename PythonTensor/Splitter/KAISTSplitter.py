from Point import Point
from Splitter.AbstractSplitter import AbstractSplitter
from PathPoint import *

class KAISTSplitter(AbstractSplitter):
    def Split(self, data, fileName):
        data = data.split('\n')
        sets = []

        currentPathPoint = PathPoint()
        for i in data:
            startPointLat = self.convertCoord(3622.244)
            startPointLon = self.convertCoord(12721.434)
            if not i == "":
                splitData = i.split('\t')
                for k in range(len(splitData)):
                    splitData[k] = splitData[k].strip()
                lat = self.addMeters(startPointLat, float(splitData[1]), True)
                lon = self.addMeters(startPointLon, float(splitData[2]))
                point = Point(int(float(splitData[0]))*1000, 0.0, lat, lon, 0, 0)
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
            
        if not currentPathPoint.getPointsCount() == 1:
            sets.append(currentPathPoint)

        jumpList = self.converToJumpList(sets)
        with open(fileName + '.txt', 'w') as f:
            for i in jumpList:
                f.write(i.departurePoint.toString() + ' ' + i.destination.toString() + ' ' + str(i.time) +  ' ' + str(i.pauseTime) + '\n')


