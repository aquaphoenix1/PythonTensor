from abc import abstractmethod
from datetime import date
from Jump import Jump
import math

class AbstractSplitter(object):
    @abstractmethod
    def split(self, data, fileName):
        pass

    def convertToDate(self, time):
        return date.fromtimestamp(int(time)/1000.0)

    def convertCoord(self, coord):
        grad = int(coord)
        g = int(grad / 100)
        m = grad - (g * 100)
        sec = int((coord - grad) * 100)
        return g + m / 60 + sec / 3600

    def converToJumpList(self, sets):
        jumpList = list()
        for i in range(len(sets) - 1):
            time = sets[i+1].getFirstPoint().date - sets[i].getLastPoint().date
            pauseTime = sets[i].getLastPoint().date - sets[i].getFirstPoint().date
            jumpList.append(Jump(sets[i].center, sets[i+1].center, time, pauseTime))

        return jumpList

    def addMeters(self, center, meters, isLat=False):
        r_earth = 6372795
        if isLat == True:
            return center  + (meters / r_earth) * (180 / math.pi);
        else:
            return center + (meters / r_earth) * (180 / math.pi) / math.cos(center * math.pi/180);
