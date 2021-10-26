from PathPoint import PathPoint

class Location(object):
    Points = None
    Boundaries = None
    r = 100
    Number = None

    def __init__(self, point, number):
        self.Points = []
        self.Points.append(point)
        self.Number = number

    def tryAdd(self, point):
        for p in self.Points:
            if PathPoint.distanceInMetersBetweenEarthCoordinates(p.latitude, p.longitude, point.latitude, point.longitude) < self.r:
                self.Points.append(point)
                return True
    
    @staticmethod
    def FindLocation(point: PathPoint, locations):
        for l in locations:
            for i in l.Points:
                if point.equal(i):
                    return l

        return None