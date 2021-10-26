import pyqtgraph as pg
from Locations.Location import Location

class Visualizer(object):
    def __init__(self, graph):
        self.graphWidget = graph
        self.graphWidget.setBackground('w')

    def getColor(self, size):
        red = size * 10
        while red > 255:
            red = red - 255
        green = size * 15
        while green > 255:
            green = green - 255
        blue = size * 20
        while blue > 255:
            blue = blue / 2

        return pg.mkPen(color=(red, green, blue))

    def getSymbol(self, size):
        while(size > 5):
            size = size - 5
        if size == 0:
            return '+'
        elif size == 1:
            return '+'
        elif size == 3:
            return '+'
        elif size == 4:
            return '+'
        else:
            return '+'

    def drawArr(self, arr):
        for i in range(len(arr)):
            self.plot(arr[i][0], arr[i][1], self.getColor(i), self.getSymbol(i))

    def plot(self, x, y, pen = pg.mkPen(color=(255, 0, 0)), symbol='+'):
        self.graphWidget.plot(x, y, pen = pen, symbol=symbol, symbolSize=30)

    def clear(self):
        self.graphWidget.clear()

    def plotLocation(self, location):
        for i in location.Boundaries:
            x = []
            y = []
            for j in i:
                x.append(j[0])
                y.append(j[1])
            self.plot(x, y, pg.mkPen(color=(100, 100, 100)), symbol='o')