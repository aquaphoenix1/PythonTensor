from PathPoint import PathPoint
from PathPoint import CentralPoint
import json

class Location(object):
    r = 30

    def __init__(self, point, number):
        self.Points = []
        if not point == None:
            self.Points.append(point)
        self.Boundaries = []
        self.Number = number

    def to_dict(u):
      dict = {
        "Points": json.dumps(u.Points, ensure_ascii=False, default=PathPoint.serialize),
        "Boundaries": u.Boundaries,
        "Number": u.Number
      }
      return dict

    def hook(obj):
        loc = Location(None, obj['Number'])
        loc.Points = json.loads(obj['Points'], object_hook=PathPoint.deserialize)
        loc.Boundaries = obj['Boundaries']
        return loc

    def newTryAdd(self, point):
        for p in self.Points:
            dx = p.center.latitude - point.center.latitude
            dy = p.center.longitude - point.center.longitude
            if dx * dx + dy * dy <= Location.r * Location.r:
                self.Points.append(point)
                return True

    def tryAdd(self, point):
        for p in self.Points:
            if PathPoint.distanceInMetersBetweenEarthCoordinates(p.latitude, p.longitude, point.latitude, point.longitude) < Location.r:
                self.Points.append(point)
                return True
    
    @staticmethod
    def FindLocation(point: PathPoint, locations):
        for l in locations:
            for i in l.Points:
                if point.equal(i.center):
                    return l

        return None