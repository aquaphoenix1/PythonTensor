import math
from sklearn.cluster import OPTICS

class Cluster(object):
    Radius = None

    def __init__(self, radius=5.0):
        self.Radius = radius

    def clusterizeData(self, data):
        #source = []
        #for d in data:
        #    source.append([d.latitude, d.longitude])
        #clustering = OPTICS(min_samples=2).fit(source)
        #labels = clustering.labels_

        #result = [None] * (labels.max() + 1)
        #for i in range(labels.max() + 1):
        #    result[i] = [];

        #for i in range(len(labels)):
        #    if labels[i] != -1:
        #        result[labels[i]].append(data[i])

        #res = []
        #for i in range(len(result)):
        #    res.append(self.combinePoints(result[i]))

        res = []
        point = data[0]
        combine = [point]

        for i in range(1, len(data)):
            distance = self.distanceInMetersBetweenEarthCoordinates(point.latitude, point.longitude, data[i].latitude, data[i].longitude)
            if distance < self.Radius:
                combine.append(data[i])
            else:
                if len(combine) == 0:
                    res.append(data[i])
                    point = data[i]
                else:
                    res.append(combine)
                    point = combine[len(combine) - 1]
                    combine = []

        if len(combine) != 0:
            res.append(combine)


        return res

    def combinePoints(self, points):
        point = points[0]
        for i in range(1, len(points)):
            #self.combineTwoPoint(point, points[i])
            pass

        return point

    def combineTwoPoint(self, point1, point2):
        point1.latitude = (point1.latitude + point2.latitude) / 2.0
        point1.latitude = (point1.longitude + point2.longitude) / 2.0

    def degreesToRadians(self, degrees):
        return degrees * math.pi / 180


    def distanceInMetersBetweenEarthCoordinates(self, lat1, lon1, lat2, lon2):
        earthRadiusKm = 6378.1370

        dLat = self.degreesToRadians(lat2 - lat1)
        dLon = self.degreesToRadians(lon2 - lon1)
        lat1 = self.degreesToRadians(lat1)
        lat2 = self.degreesToRadians(lat2)
        a = math.pow(math.sin(dLat / 2.0), 2) + math.pow(math.sin(dLon / 2.0), 2) * math.cos(lat1) * math.cos(lat2)
        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) 
        return earthRadiusKm * c * 1000;