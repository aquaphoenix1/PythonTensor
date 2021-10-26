import math
from sklearn.cluster import OPTICS

class Cluster(object):
    Radius = None

    def __init__(self, radius=100):
        self.Radius = radius

    def clusterizeData(self, data):
        result = []



        return result