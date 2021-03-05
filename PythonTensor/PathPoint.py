import math

class PathPoint(object):
    RADIUS = 5
    MAX_TIME = 30

    pointsList = None
    center = None

    def __init__(self):
        self.pointsList = list()
        self.center = CentralPoint(0, 0)

    def getPointsCount(self):
        return len(self.pointsList)

    def getFirstPoint(self):
        return self.pointsList[0]

    def getLastPoint(self):
        return self.pointsList[self.getPointsCount() - 1]

    def addPoint(self, point):
        self.pointsList.append(point)
        self.recalculateCenter()

    def recalculateCenter(self):
        lat = 0.0
        lon = 0.0

        for i in self.pointsList:
            lat = lat + i.latitude
            lon = lon + i.longitude

        length = self.getPointsCount()

        self.center = CentralPoint(lat / length, lon / length)

    def isInsideRadius(self, point):
        if self.getPointsCount() == 0:
            return True

        distance = self.distanceInMetersBetweenEarthCoordinates(point.latitude, point.longitude, self.center.latitude, self.center.longitude)
        
        if(distance > 1 and distance < self.RADIUS):
            sf = 0
        
        return distance < self.RADIUS

    def degreesToRadians(self, degrees):
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
            self.recalculateCenter()
            if self.getPointsCount() == 1 or self.isAllInsideRadius():
                break

    def distanceInMetersBetweenEarthCoordinates(self, lat1, lon1, lat2, lon2):
        earthRadiusKm = 6372795

        dPhi = self.degreesToRadians(lat2 - lat1)
        dLyambda = self.degreesToRadians(lon2 - lon1)
        phi1 = self.degreesToRadians(lat1)
        phi2 = self.degreesToRadians(lat2)
        a = math.pow(math.sin(dPhi / 2.0), 2) + math.pow(math.sin(dLyambda / 2.0), 2) * math.cos(phi1) * math.cos(phi2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
        return earthRadiusKm * c;

    def isMoreTime(self):
        return False if self.getPointsCount() == 1 else (self.pointsList[self.getPointsCount() - 1].date - self.pointsList[0].date) > self.MAX_TIME * 1000

    def calculateTime(self):
        self.pauseTime = self.pointsList[0].date if self.getPointsCount() == 1 else self.pointsList[self.getPointsCount() - 1].date - self.pointsList[0].date

class CentralPoint(object):
    latitude = 0
    longitude = 0

    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon

    def toString(self):
        return str(self.latitude) + ' ' + str(self.longitude);
