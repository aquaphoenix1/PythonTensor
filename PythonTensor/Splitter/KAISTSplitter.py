from Point import Point
from Splitter.AbstractSplitter import AbstractSplitter
from PathPoint import *
import sys
import math
from Jump import Jump
import copy

class KAISTSplitter(AbstractSplitter):
    minX = sys.maxsize
    maxX = -sys.maxsize - 1
    minY = sys.maxsize
    maxY = -sys.maxsize - 1

    def Split(self, data, fileName, num):
        #data = data.split('\n')
        #sets = []

        #currentPathPoint = PathPoint()
        #currentPathPoint.center.number = num
        #num = num + 1
        #for i in data:
        #    #startPointLat = self.convertCoord(3622.244)
        #    #startPointLon = self.convertCoord(12721.434)
        #    if not i == "":
        #        splitData = i.split('\t')
        #        for k in range(len(splitData)):
        #            splitData[k] = splitData[k].strip()
        #        #lat = self.addMeters(startPointLat, float(splitData[1]), True)
        #        #lon = self.addMeters(startPointLon, float(splitData[2]))
        #        point = Point(int(float(splitData[0]))*1000, 0.0, float(splitData[1]), float(splitData[2]), 0, 0)
        #        currentPathPoint.addPoint(point)
        #        if currentPathPoint.isOutOfRange():
        #            if currentPathPoint.stopTimeReached():
        #                last = currentPathPoint.popLast()
        #                sets.append(currentPathPoint)

        #                if currentPathPoint.center.latitude < self.minX:
        #                    self.minX = currentPathPoint.center.latitude
        #                if currentPathPoint.center.latitude > self.maxX:
        #                    self.maxX = currentPathPoint.center.latitude

        #                if currentPathPoint.center.longitude < self.minY:
        #                    self.minY = currentPathPoint.center.longitude
        #                if currentPathPoint.center.longitude > self.maxY:
        #                    self.maxY = currentPathPoint.center.longitude

        #                currentPathPoint = PathPoint()
        #                currentPathPoint.center.number = num
        #                num = num + 1
        #                currentPathPoint.addPoint(last)
        #            else:
        #                currentPathPoint.recalculateNew()

        #if currentPathPoint.getPointsCount() > 0:
        #    sets.append(currentPathPoint)

        #jumps = self.converToJumpList(sets)
        ##for i in range(len(sets) - 1):
        ##    jumps.append(Jump(sets[i].center, sets[i+1].center, sets[i+1].getFirstPoint().date - sets[i].getLastPoint().date, sets[i+1].getLastPoint().date - sets[i+1].getFirstPoint().date))
        data = data.split('\n')
        for i in range(len(data)):
            if not data[i] == "":
                splitData = data[i].split('\t')
                for k in range(len(splitData)):
                    splitData[k] = splitData[k].strip()
                data[i] = Point(int(float(splitData[0])), 0.0, float(splitData[1]), float(splitData[2]), 0, 0)
        
        #x1 = []
        #y1 = []
        #for i in range(23, 181):
        #    x1.append(data[i].latitude)
        #    y1.append(data[i].longitude)

        currentPathPoint = PathPoint()
        sets = []
        i = -1
        while True:
            i+=1
            while(currentPathPoint.newAddPoint(data, i) and not currentPathPoint.isOutOfRange()):
                i+=1
            if currentPathPoint.stopTimeReached():
                x = (currentPathPoint.sumX - currentPathPoint.xcoord[len(currentPathPoint.xcoord) - 1]) / (len(currentPathPoint.xcoord) - 1)
                y = (currentPathPoint.sumY - currentPathPoint.ycoord[len(currentPathPoint.ycoord) - 1]) / (len(currentPathPoint.ycoord) - 1)
                currentPathPoint.center = CentralPoint(x, y, num)
                currentPathPoint.set()

                if currentPathPoint.center.latitude < self.minX:
                    self.minX = currentPathPoint.center.latitude
                if currentPathPoint.center.latitude > self.maxX:
                    self.maxX = currentPathPoint.center.latitude

                if currentPathPoint.center.longitude < self.minY:
                    self.minY = currentPathPoint.center.longitude
                if currentPathPoint.center.longitude > self.maxY:
                    self.maxY = currentPathPoint.center.longitude

                num = num + 1
                sets.append(currentPathPoint)
                currentPathPoint = currentPathPoint.getCopy()
                while (len(currentPathPoint.xcoord) > 1):
                    currentPathPoint.removePoint()
            else:
                while (currentPathPoint.removePoint() and currentPathPoint.isOutOfRange()):
                    pass
            if i == len(data) - 1:
                if currentPathPoint.getPointsCount() > 1:
                    x = (currentPathPoint.sumX - currentPathPoint.xcoord[len(currentPathPoint.xcoord) - 1]) / (len(currentPathPoint.xcoord) - 1)
                    y = (currentPathPoint.sumY - currentPathPoint.ycoord[len(currentPathPoint.ycoord) - 1]) / (len(currentPathPoint.ycoord) - 1)
                    currentPathPoint.center = CentralPoint(x, y, num)
                    currentPathPoint.set()
                    num = num + 1
                break

        jumps = self.converToJumpList(sets)

        return sets, jumps, num
    #, jumps, num
