import pyqtgraph as pg

class Visualizer(object):
    def __init__(self, graph):
        self.graphWidget = graph
        self.graphWidget.setBackground('w')

    def plot(self, x, y, pen = pg.mkPen(color=(255, 0, 0))):
        self.graphWidget.plot(x, y, pen = pen, symbol='+', symbolSize=30)

    def clear(self):
        self.graphWidget.clear()