from Locations.Location import Location
from scipy.spatial import Delaunay
import numpy as np
from PathPoint import CentralPoint
from PathPoint import PathPoint
import math

class LocationsCalculator(object):
    locations = None

    def calcN(self, data):
        locs = []
        d = data.copy()
        num = 0
        while (len(d) > 0):
            location = Location(None, num)
            num += 1
            for i in d:
                if self.isMergeable(location.Points, [i]):
                    location.Points.append(i)
                    d.remove(i)
            self.calculateBoundaries(location)
            locs.append(location)
            location = None
        if not location == None and len(location.Points) > 0:
            self.calculateBoundaries(location)
            locs.append(location)
        LocationsCalculator.locations = locs
        return locs


    def calcNewLocations(self, Xmin, Xmax, Ymin, Ymax, data):
        Delta = 70
        Xmin=math.floor(Xmin/Delta)*Delta
        Xmax=math.ceil(Xmax/Delta)*Delta
        Xsize=math.ceil((Xmax-Xmin)/Delta)
        Ymin=math.floor(Ymin/Delta)*Delta
        Ymax=math.ceil(Ymax/Delta)*Delta
        Ysize=math.ceil((Ymax-Ymin)/Delta)

        locations = []
        for i in range(Ysize):
            arr = []
            for j in range(Xsize):
                arr.append([])
            locations.append(arr)

        for d in data:
            for j in d:
                i=math.floor((j.center.longitude-Ymin)/Delta)
                k=math.floor((j.center.latitude-Xmin)/Delta)
                locations[i][k].append(j)

        indexesX = []
        indexesY = []

        for i in range(Ysize):
            for k in range(Xsize):
                if len(locations[i][k]) > 0:
                    indexesX.append(i)
                    indexesY.append(k)
        a = []
        res = []
        num = 0
        while len(indexesX) > 0:
            location = Location(None, num)
            num += 1
            self.mergeClusterToHotSpot(location, locations[indexesX[0]][indexesY[0]])
            indexesX.pop(0)
            indexesY.pop(0)
            j = 0
            while j < len(indexesX):
                if self.isMergeable(location.Points, locations[indexesX[j]][indexesY[j]]):
                    self.mergeClusterToHotSpot(location, locations[indexesX[j]][indexesY[j]])
                    indexesX.pop(j)
                    indexesY.pop(j)
                else:
                    j += 1

            self.calculateBoundaries(location)
            a.append(len(location.Points))
            res.append(location)
        LocationsCalculator.locations = res
        #a = []
        #for i in [x.Points for x in res]:
        #    for j in i:
        #        a.append(j.center.number)
        return res

    def isMergeable(self, wps1, wps2):
        if len(wps1) == 0 or len(wps2) == 0:
            return True

        for i in range(len(wps1)):
            for j in range(len(wps2)):
                dx = wps1[i].center.latitude - wps2[j].center.latitude
                dy = wps1[i].center.longitude - wps2[j].center.longitude
                if dx * dx + dy * dy <= 100 * 100:
                    return True
        return False

    def mergeClusterToHotSpot(self, location, wps):
        if len(wps) == 0:
            return

        for i in range(len(wps)):
            location.Points.append(wps[i])

    def calculate(self, data):
        v = data.copy()
        locations = []
        add = False
        location = None
        num = 0
        source = len(v)
        while not len(v) == 0:
            print('Remaining ' + str(len(v)) + ' of ' + str(source))
            if not add:
                if not location == None:
                    locations.append(location)
                    self.calculateBoundaries(location)

                location = Location(v[0], num)
                num = num + 1
                v.pop(0)
            
            add = False
            for i in v:
                if(location.newTryAdd(i)):
                    v.remove(i)
                    add = True
        
        if not location.Points == 0:
            locations.append(location)
            self.calculateBoundaries(location)

        LocationsCalculator.locations = locations

        return LocationsCalculator.locations

    def makeRectBoundaries(self, location):
        mostLeft = location.Points[0].center.latitude
        mostRight = location.Points[0].center.latitude
        mostTop = location.Points[0].center.longitude
        mostBottom = location.Points[0].center.longitude
        for i in location.Points:
            if i.center.latitude < mostLeft:
                mostLeft = i.center.latitude
            if i.center.latitude > mostRight:
                mostRight = i.center.latitude
            if i.center.longitude < mostBottom:
                mostBottom = i.center.longitude
            if i.center.longitude > mostTop:
                mostTop = i.center.longitude
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
            points.append([i.center.latitude, i.center.longitude])

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
        