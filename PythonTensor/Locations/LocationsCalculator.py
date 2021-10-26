from Locations.Location import Location
from scipy.spatial import Delaunay
import numpy as np
from PathPoint import CentralPoint
from PathPoint import PathPoint

class LocationsCalculator(object):
    locations = None

    def calculate(self, data):
        v = data
        locations = []
        add = False
        location = None
        num = 0
        while not len(v) == 0:
            if not add:
                if not location == None:
                    locations.append(location)
                    self.calculateBoundaries(location)

                location = Location(v[0], num)
                num = num + 1
                v.pop(0)
            
            add = False
            for i in v:
                if(location.tryAdd(i)):
                    v.remove(i)
                    add = True
        
        if not location.Points == 0:
            locations.append(location)
            self.calculateBoundaries(location)

        LocationsCalculator.locations = locations

        return LocationsCalculator.locations

    def makeRectBoundaries(self, location):
        mostLeft = location.Points[0].latitude
        mostRight = location.Points[0].latitude
        mostTop = location.Points[0].longitude
        mostBottom = location.Points[0].longitude
        for i in location.Points:
            if i.latitude < mostLeft:
                mostLeft = i.latitude
            if i.latitude > mostRight:
                mostRight = i.latitude
            if i.longitude < mostBottom:
                mostBottom = i.longitude
            if i.longitude > mostTop:
                mostTop = i.longitude
        location.Boundaries = [[[mostLeft, mostTop], [mostRight, mostTop], [mostRight, mostBottom], [mostLeft, mostBottom], [mostLeft, mostTop]]]
      
    @staticmethod
    def getNextPointBetweenPointAndLocation(point, number):
        location = next((x for x in LocationsCalculator.locations if x.Number == number), None)
        most = -1
        loc = None
        if (len(location.Boundaries) > 1):
            for i in location.Boundaries:
                c = LocationsCalculator.getCenter(i)
                dist = PathPoint.distanceInMetersBetweenEarthCoordinates(point.latitude, point.longitude, c.latitude, c.longitude)
                if most == -1 or dist < most and not dist == 0:
                    most = dist
                    loc = c
        else:
            loc = LocationsCalculator.getCenter(location.Boundaries[0])

        return loc

    @staticmethod
    def getCenter(boundaries):
        ux = 0
        uy = 0
        for i in boundaries:
            ux = ux + i[0]
            uy = uy + i[1]

        ux = ux / len(boundaries)
        uy = uy / len(boundaries)

        return CentralPoint(ux, uy, -1)

    def calculateBoundaries(self, location):
        location.Boundaries = []
        points = []
        for i in location.Points:
            points.append([i.latitude, i.longitude])

        points = np.array(points)
        try:
            tri = Delaunay(points)
        except Exception as e:
            self.makeRectBoundaries(location)
            return
        connections = points[tri.simplices]
        for c in connections:
            con = []
            for i in c:
                con.append(list(i))
            con.append(list(c[0]))
            location.Boundaries.append(con)
        