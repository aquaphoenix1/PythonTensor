import math

class PathPoint(object):
    RADIUS = 5
    MAX_TIME = 30

    pointsList = None
    center = None

    def __init__(self):
        self.pointsList = list()
        self.center = CentralPoint(0, 0)

    def addPoint(self, point):
        self.pointsList.append(point)
        self.recalculateCenter()

    def recalculateCenter(self):
        lat = 0.0
        lon = 0.0

        for i in self.pointsList:
            lat = lat + i.latitude
            lon = lon + i.longitude

        length = len(self.pointsList)

        self.center = CentralPoint(lat / length, lon / length)

    def isInsideRadius(self, point):
        if(len(self.pointsList) == 0):
            return True

        d = math.sqrt(math.pow(point.latitude - self.center.latitude, 2) + math.pow(point.longitude - self.center.longitude, 2))

        distance = self.distanceInMetersBetweenEarthCoordinates(point.latitude, point.longitude, self.center.latitude, self.center.longitude)
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
            if len(self.pointsList) == 1 or self.isAllInsideRadius():
                break

    def distanceInMetersBetweenEarthCoordinates(self, lat1, lon1, lat2, lon2):
        earthRadiusKm = 6371e3

        dPhi = self.degreesToRadians(lat2 - lat1)
        dLyambda = self.degreesToRadians(lon2 - lon1)
        phi1 = self.degreesToRadians(lat1)
        phi2 = self.degreesToRadians(lat2)
        a = math.pow(math.sin(dPhi / 2.0), 2) + math.pow(math.sin(dLyambda / 2.0), 2) * math.cos(phi1) * math.cos(phi2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
        return earthRadiusKm * c;

    def isMoreTime(self):
        return False if len(self.pointsList) == 1 else (self.pointsList[len(self.pointsList) - 1].date - self.pointsList[0].date) > self.MAX_TIME * 1000

class CentralPoint(object):
    latitude = 0
    longitude = 0

    def __init__(self, lat, lon):
        self.latitude = lat
        self.longitude = lon
