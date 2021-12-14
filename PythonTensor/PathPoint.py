import math
from Point import Point
import json

class PathPoint(object):
    RADIUS = 5
    MAX_TIME = 30

    def __init__(self):
        self.pointsList = list()
        self.center = CentralPoint(0, 0, 0)
        self.sumX = 0
        self.sumY = 0
        self.xcoord = []
        self.ycoord = []
        self.time = []
        self.tMin = 0
        self.tMxB = 0
        self.tMax = 0

    def serialize(obj):
        return {
            "pointsList": json.dumps(obj.pointsList, ensure_ascii=False, default=Point.serialize),
            "sumX": obj.sumX,
            "sumY": obj.sumY,
            "tMax": obj.tMax,
            "tMin": obj.tMin,
            "tMxB": obj.tMxB,
            "time": obj.time,
            "xcoord": obj.xcoord,
            "ycoord": obj.ycoord,
            "center": json.dumps(obj.center, ensure_ascii=False, default=CentralPoint.serialize)
            }

    def deserialize(obj):
        p = PathPoint()
        p.pointsList = json.loads(obj["pointsList"], object_hook=Point.deserialize)
        p.sumX = obj["sumX"]
        p.sumY = obj["sumY"]
        p.tMax = obj["tMax"]
        p.tMin = obj["tMin"]
        p.tMxB = obj["tMxB"]
        p.time = obj["time"]
        p.xcoord = obj["xcoord"]
        p.ycoord = obj["ycoord"]
        p.center = json.loads(obj["center"], object_hook=CentralPoint.deserialize)
        return p

    def recalculateNew(self):
        self.removeFirstPoint()

        while self.getPointsCount() > 1 and self.isOutOfRange():
            self.removeFirstPoint()

    def removePoint(self):
        if (len(self.xcoord) > 1):
            self.sumX -= self.xcoord[0]
            self.xcoord.pop(0)
            self.sumY -= self.ycoord[0]
            self.ycoord.pop(0)
            self.time.pop(0)
            self.tMin = self.time[0]
            if (len(self.xcoord) == 1):
               self.tMxB = self.tMax
            return True
        else:
            return False

    def popLast(self):
        last = self.pointsList.pop(self.getPointsCount() - 1)
        self.recalculateCenter()
        return last

    def stopTimeReached(self):
        return self.tMxB - self.tMin > 30
        #return self.getLastPoint().date - self.getFirstPoint().date > PathPoint.MAX_TIME * 1000

    def getPointsCount(self):
        return len(self.pointsList)

    def getFirstPoint(self):
        return self.pointsList[0]

    def getLastPoint(self):
        return self.pointsList[self.getPointsCount() - 1]

    def addPoint(self, point):
        self.pointsList.append(point)
        self.recalculateCenter()

    def getCopy(self):
        p = PathPoint()
        p.sumX = self.sumX
        p.sumY = self.sumY
        p.xcoord = self.xcoord.copy()
        p.ycoord = self.ycoord.copy()
        p.time = self.time.copy()
        p.tMin = self.tMin
        p.tMxB = self.tMxB
        p.tMax = self.tMax
        return p
        
    def newAddPoint(self, points, index):
        if len(points) <= index or points[index] == "":
            return False

        p = points[index]
        self.xcoord.append(p.latitude)
        self.sumX = self.sumX + p.latitude
        self.ycoord.append(p.longitude)
        self.sumY = self.sumY + p.longitude
        self.time.append(p.date)
        if len(self.xcoord) == 1:
            self.tMin = p.date
            self.tMxB = p.date
            self.tMax = p.date
        else:
            self.tMxB = self.tMax
            self.tMax = p.date

        return True

    def set(self):
        for i in range(len(self.xcoord) - 1):
            self.pointsList.append(Point(self.time[i], 0, self.xcoord[i], self.ycoord[i], 0, 0))

    def isOutOfRange(self):
        #if self.getPointsCount() > 0:
        #    #if PathPoint.distanceInMetersBetweenEarthCoordinates(self.getLastPoint().latitude, self.getLastPoint().longitude, self.center.latitude, self.center.longitude) > PathPoint.RADIUS:
        #    dx = self.getLastPoint().latitude - self.center.latitude
        #    dy = self.getLastPoint().longitude - self.center.longitude
        #    if dx*dx + dy*dy > PathPoint.RADIUS * PathPoint.RADIUS:
        #        return True
        
        #copy = self.pointsList.copy()
        #xwp = self.center.latitude
        #ywp = self.center.longitude

        #while len(copy) > 1:
        #    #distance = PathPoint.distanceInMetersBetweenEarthCoordinates(copy[0].latitude, copy[0].longitude, xwp, ywp)
        #    dx = copy[0].latitude - xwp
        #    dy = copy[0].longitude - ywp
        #    if dx * dx + dy * dy <= PathPoint.RADIUS * PathPoint.RADIUS:
        #        copy.pop(0)
        #    else:
        #        return True

        #return False
        xc = self.xcoord.copy()
        yc = self.ycoord.copy()
        if len(self.xcoord) > 0:
            xwp = self.sumX / len(self.xcoord)
            ywp = self.sumY / len(self.ycoord)
            dx = xc[len(xc)-1] - xwp
            dy = yc[len(yc)-1] - ywp
            if (dx * dx + dy * dy > 25):
                return True
        while (len(xc) > 1):
            dx = xc[0] - xwp
            dy = yc[0] - ywp
            if (dx * dx + dy * dy <= 25):
                xc.pop(0)
                yc.pop(0)
            else:
                return True
        return False

    def recalculateCenter(self):
        lat = 0.0
        lon = 0.0

        for i in self.pointsList:
            lat = lat + i.latitude
            lon = lon + i.longitude

        length = self.getPointsCount()

        self.center = CentralPoint(lat / length, lon / length, self.center.number)

    def isInsideRadius(self, point):
        if self.getPointsCount() == 0:
            return True

        distance = PathPoint.distanceInMetersBetweenEarthCoordinates(point.latitude, point.longitude, self.center.latitude, self.center.longitude)
        
        return distance < PathPoint.RADIUS
    
    @staticmethod
    def degreesToRadians(degrees):
        return degrees * math.pi / 180.0

    def isAllInsideRadius(self):
        for i in self.pointsList:
            if(not self.isInsideRadius(i)):
                return False

        return True

    def removeFirstPoint(self):
        self.pointsList.pop(0)
        self.recalculateCenter()

    def recalculate(self):
        while True:
            self.removeFirstPoint()
            if self.getPointsCount() == 1 or self.isAllInsideRadius():
                break

    @staticmethod
    def distanceInMetersBetweenEarthCoordinates(lat1, lon1, lat2, lon2):
        #earthRadiusKm = 6372795

        #dPhi = PathPoint.degreesToRadians(lat2 - lat1)
        #dLyambda = PathPoint.degreesToRadians(lon2 - lon1)
        #phi1 = PathPoint.degreesToRadians(lat1)
        #phi2 = PathPoint.degreesToRadians(lat2)
        #a = math.pow(math.sin(dPhi / 2.0), 2) + math.pow(math.sin(dLyambda / 2.0), 2) * math.cos(phi1) * math.cos(phi2)
        #c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
        #return earthRadiusKm * c;

        return math.sqrt(pow(lat1-lat2, 2) + pow(lon1-lon2, 2))

    def isMoreTime(self):
        return False if self.getPointsCount() == 1 else (self.pointsList[self.getPointsCount() - 1].date - self.pointsList[0].date) > PathPoint.MAX_TIME * 1000

    def calculateTime(self):
        self.pauseTime = self.pointsList[0].date if self.getPointsCount() == 1 else self.pointsList[self.getPointsCount() - 1].date - self.pointsList[0].date

class CentralPoint(object):
    def __init__(self, lat, lon, num):
        self.latitude = lat
        self.longitude = lon
        self.number = num

    def serialize(obj):
        return {
            "latitude": obj.latitude,
            "longitude": obj.longitude,
            "number": obj.number
            }

    def deserialize(obj):
        try:
            return CentralPoint(obj['latitude'], obj['longitude'], obj['number'])
        except:
            return [obj['Locations'], obj['Time'], obj['Points']]
    def toString(self):
        return str(self.latitude) + ' ' + str(self.longitude);

    def equal(self, point):
        #return self.latitude == point.latitude and self.longitude == point.longitude
        return self.number == point.number