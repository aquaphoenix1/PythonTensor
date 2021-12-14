import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import UI  # Это наш конвертированный файл дизайна
from Splitter.Splitter import Splitter
from Splitter.KAISTSplitter import KAISTSplitter
from Clusterizer.Cluster import Cluster
from SetListModel import SetListModel
import pyqtgraph as pg
from PyQt5 import QtCore
from Visualizer import Visualizer
from Jump import Jump
from PathPoint import CentralPoint
from NetworkController import NetworkController
from Locations.LocationsCalculator import LocationsCalculator
from Parser.DARTParser import DARTParser
from Parser.KAISTParser import KAISTParser
from Locations.Location import Location
from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from CharacteristicCalculators.Plotter import Plotter
import matplotlib.pyplot as plt
import os

import numpy as np

import json

class ExampleApp(QtWidgets.QMainWindow, UI.Ui_MainWindow):
    Controller = NetworkController()

    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        super().__init__()
        self.setupUi(self)
        self.pushButtonConvert.clicked.connect(self.convert_click)
        self.pushButtonDeserialize.clicked.connect(self.deserialize)
        self.pushButtonSerialize.clicked.connect(self.serialize)
        self.pushButtonPlotTrain.clicked.connect(self.plotTrain)
        self.pushButtonInit.clicked.connect(self.netInit)
        self.pushButtonTrain.clicked.connect(self.train_click)
        #self.pushButtonTesting.clicked.connect(self.testing_click)
        self.pushButtonGenerate.clicked.connect(self.testing_click)
        self.pushButtonNetSerialize.clicked.connect(self.pushButtonNetSerializeClick)
        self.pushButtonNetDeserialize.clicked.connect(self.pushButtonNetDeserializeClick)
        self.pushButtonAddGraph.clicked.connect(self.pushButtonAddGraphClick)
        self.pushButtonClearGraph.clicked.connect(self.pushButtonClearGraphClick)
        self.pushButtonPlotNewWindow.clicked.connect(self.pushButtonPlotNewWindowClick)
        self.model = SetListModel()
        #self.listView_6.setModel(self.model)
        #self.listView_6.selectionModel().selectionChanged.connect(self.listChangedEvent)
        #graphWidget = pg.PlotWidget()
        #self.verticalLayoutVisualize.addWidget(graphWidget)
        #self.sourceVisualizer = Visualizer(graphWidget)

        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.tabWidgetGraph.currentChanged.connect(self.tabWidgetGraphChanged)
        self.checkBoxPlotTrained.clicked.connect(self.checkBoxPlotTrainedClick)

        fig = Plotter.initFigure()
        self.plotWidget = FigureCanvas(Plotter.fig)
        lay = QtWidgets.QVBoxLayout(self.verticalWidget)  
        lay.setContentsMargins(0, 0, 0, 0)      
        lay.addWidget(self.plotWidget)

        self.bar = None
        
        #graphWidget = pg.PlotWidget()
        #self.listView.setModel(self.model)
        #self.clusterVisualizer = Visualizer(graphWidget);

    def pushButtonPlotNewWindowClick(self):
        d = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', 'C:/Users/aqua_/source/repos/PythonTensor/PythonTensor/generated')
        if(len(d[0]) != 0):
            res = []
            for fname in d[0]:
                with open(fname, 'r') as f:
                    obj = json.load(f, object_hook=CentralPoint.deserialize)
                    res.append(obj)
            Plotter.plot(res, self.Controller.locationsCount, self.Controller.minTime, self.Controller.maxTime, self.Controller.minPauseTime, self.Controller.maxPauseTime, self.Controller.levyCoeff, 'softmax')

    def pushButtonClearGraphClick(self):
        Plotter.clear()

        state = self.checkBoxPlotTrained.checkState()
        if state == 2:
            Plotter.plotT(self.tabWidgetGraph.currentIndex())

    def checkBoxPlotTrainedClick(self):
        self.tabWidgetGraphChanged(-1)

    def pushButtonAddGraphClick(self):
        d = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', 'C:/Users/aqua_/source/repos/PythonTensor/PythonTensor/generated')
        if(len(d[0]) != 0):
            Plotter.clearGraph()
            res = []
            for fname in d[0]:
                with open(fname, 'r') as f:
                    obj = json.load(f, object_hook=CentralPoint.deserialize)
                    res.append(obj)
            Plotter.appendData(res)
            state = self.checkBoxPlotTrained.checkState()
            if state == 2:
                Plotter.plotT(self.tabWidgetGraph.currentIndex())
            Plotter.plotG(self.tabWidgetGraph.currentIndex(), self.Controller.locationsCount, self.Controller.minTime, self.Controller.maxTime, self.Controller.minPauseTime, self.Controller.maxPauseTime, self.Controller.levyCoeff)

    def tabChanged(self, num):
        if num == 1:
            self.bar = NavigationToolbar(self.plotWidget, self)
            self.addToolBar(QtCore.Qt.BottomToolBarArea, self.bar)
        else:
            if not self.bar == None:
                self.removeToolBar(self.bar)
                self.bar = None

    def tabWidgetGraphChanged(self, num):
        Plotter.clearGraph()

        state = self.checkBoxPlotTrained.checkState()
        if state == 2:
            Plotter.plotT(self.tabWidgetGraph.currentIndex())
        Plotter.plotG(self.tabWidgetGraph.currentIndex(), self.Controller.locationsCount, self.Controller.minTime, self.Controller.maxTime, self.Controller.minPauseTime, self.Controller.maxPauseTime, self.Controller.levyCoeff)


    def netInit(self):
        window = 5#int(self.textEditWindow.toPlainText())
        self.Controller.Network.init(self.Controller.getWindowSize(), self.Controller.getFeaturesCount(), self.Controller.getLocationsCount(), self.Controller.histCount, self.Controller.lastLocationsWindow)

    def browse_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'C:/Users/aqua_/source/repos/GPSConverter/GPSConverter/bin/Debug/ConvertedData/')[0]
        self.textEditFilePath.setText(fname)

    def loadTraining_click(self):
        d = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', 'C:/Users/aqua_/source/repos/PythonTensor/PythonTensor/Data/ConvertedData/KAIST')

        data = []
        points = []
        num = -1

        if(len(d[0]) != 0):
            for fname in d[0]:
                with open(fname, 'r') as f:
                    content = f.read()
                    arr = []
                    plotData = []
                    num = num + 1

                    if content.split('\n')[0].find('\t') == -1:
                        num = DARTParser.parse(content, num, plotData, points, arr)
                    else:
                        num = KAISTParser.parse(content, num, plotData, points, arr) ##########не нужно?

                    data.append(arr)

        else:
            return

        locations = LocationsCalculator().calculate(points)        

        #self.plot(data)
        #self.plotLocations(locations)
        self.Controller.setTrainData(data, locations)

        self.pushButtonClearGraphClick()
        #self.fillTable(plotData)

    def serialize(self):
        with open('locations.txt', 'w+') as f:
            json.dump(LocationsCalculator.locations, f, ensure_ascii=False, default=Location.to_dict)

        with open('data.txt', 'w+') as f:
            json.dump(self.Controller.trainPoints, f, ensure_ascii=False, default=Jump.to_dict)

    def deserialize(self):
        with open('locations.txt', 'r') as f:
            locations = json.load(f, object_hook=Location.hook)

        with open('data.txt', 'r') as f:
            data = json.load(f, object_hook=Jump.hook)

        #self.plot(data)
        #self.plotLocations(locations)
        window = int(self.textBrowserWindow.toPlainText())
        self.Controller.setTrainData(data, locations, window)
        LocationsCalculator.locations = locations

        self.pushButtonClearGraphClick()
        #self.fillTable(plotData)

    def testing_click(self):
        #count = int(self.textEditTestingCount.toPlainText())
        #startPoints = self.textEditTestingStart.toPlainText().split('\n')
        #data = []
        #for i in range(len(startPoints)):
        #    if not startPoints[i] == '':
        #        point = startPoints[i].split(' ')
        #        for k in range(len(point)):
        #            point[k] = float(point[k])
        #        #a = Controller.Network.normalize([point])
        #        data.append(point)

        self.Controller.generate(self.Controller.generateLocationsArray, self.Controller.generateParametersArray)
        #result = Controller.Network.normalizer.Denormalize(result)

        #jumpList = []
        #for i in range(len(result)):
        #    firstPoint = CentralPoint(result[0], result[1])
        #    secondPoint = CentralPoint(result[2], result[3])

        #    if len(jumpList) == 0:
        #        jumpList.append(firstPoint)
        #    jumpList.append(secondPoint)

        #self.plot(jumpList)
        #self.fillTable(jumpList)


    def fillTable(self, data):
        self.clearList()
        self.model.insertRows(0, len(data), data)


    def convert_click(self):
        d = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', 'C:/Users/aqua_/source/repos/PythonTensor/PythonTensor/Data/KAIST')
        window = int(self.textBrowserWindow.toPlainText())
        splitter = KAISTSplitter()

        sets = []
        jumps = []
        num = 0

        a = []

        for i in d[0]:
            name = i#self.textEditFilePath.toPlainText() #i
            f = open(name, 'r')
            content = f.read()
            f.close()
            if not content.split('\n')[0].find('\t') == -1:
                points, jump, num = splitter.Split(content, name, num)
                if not len(jump) == 0:
                    sets.append(points)
                    jumps.append(jump)
                    a.append(len(points))
            else:
                Splitter().Split(content, name)

        #x = []
        #y = []
        #for i in sets:
        #    for j in i:
        #        x.append(j.center.latitude)
        #        y.append(j.center.longitude)
        
        #plt.plot(x, y, 's', marker='o', label='Lyakishev: ' + str(len(x)))
        #x = []
        #y = []
        #with open('Privalov.wpt', 'r') as f:
        #    for e in f:
        #        e = e.split('\t')
        #        x.append(float(e[0]))
        #        y.append(float(e[1]))
        #plt.plot(x, y, 's', marker='o', label='Privalov: ' + str(len(x)))
        #x = []
        #y = []
        #with open('Tsarev.wpt', 'r') as f:
        #    for e in f:
        #        e = e.split('\t')
        #        x.append(float(e[0]))
        #        y.append(float(e[1]))
        #plt.plot(x, y, 's', marker='o', label='Tsarev: ' + str(len(x)))


        #plt.xticks(np.arange(-4000, 6000, 1000))
        #plt.legend()
        #plt.show()

        #locations = LocationsCalculator().calcNewLocations(splitter.minX, splitter.maxX, splitter.minY, splitter.maxY, sets)
        s = []
        for i in sets:
            s = s + i
        #locations = LocationsCalculator().calcN(s)
        locations = LocationsCalculator().calculate(s)

        self.Controller.setTrainData(jumps, locations, window)

        self.pushButtonClearGraphClick()

    def plot(self, content):
        arr = []
        for k in range(len(content)):
            x = []
            y = []
            for i in range(len(content[k])):
                if i == 0:
                    x.append(content[k][i].departurePoint.latitude)
                    y.append(content[k][i].departurePoint.longitude)
                x.append(content[k][i].destination.latitude)
                y.append(content[k][i].destination.longitude)
            arr.append([x, y])

        self.sourceVisualizer.clear()
        #self.sourceVisualizer.drawArr(arr)

    def plotLocations(self, locations):
        for loc in locations:
            self.sourceVisualizer.plotLocation(loc)

    def clearList(self):
        self.model.deleteRows(0)

    currentData = None

    def listChangedEvent(self, prev, current):
        data = self.model.getData(self.listView_6.selectedIndexes()[0].row())
        x = []
        y = []
        d = data.pointsList
        for i in range(len(d)):
            x.append(d[i].latitude)
            y.append(d[i].longitude)

        self.currentData = data

        self.sourceVisualizer.clear()
        self.sourceVisualizer.plot(x, y)
        #self.sourceVisualizer.plot([data.center.latitude],
        #[data.center.longitude], pg.mkPen(color=(0, 0, 255)))

        self.labelSource.setText(str(len(x)))


        # Network().loadDataset(data)

    def plotTrain(self):
        self.Controller.plotTrain()

    def pushButtonGenerateClick(self):
        pass

    def pushButtonNetSerializeClick(self):
        self.Controller.Network.serialize()
        
        with open('characteristics', 'w+') as f:
            json.dump({"locations": self.Controller.getLocationsCount(), 'window': self.Controller.getWindowSize(), 'stopWindow': self.Controller.lastLocationsWindow}, f)

    def pushButtonNetDeserializeClick(self):
        self.Controller.Network.load()

        with open('characteristics', 'r') as f:
            obj = json.load(f)
            self.Controller.locationsCount = obj['locations']
            self.Controller.Network.locationsCount = obj['locations']
            self.Controller.Network.stopWindow = obj['stopWindow']
            self.Controller.window = obj['window']
            self.Controller.Network.window = obj['window']

    def train_click(self):
        trainPercent = 100#int(self.textEditTrainPercent_2.toPlainText())
        self.Controller.Network.train(self.Controller.getTrainData(), trainPercent, self.Controller.minTime, self.Controller.maxTime, self.Controller.minPauseTime, self.Controller.maxPauseTime, self.Controller.lastLocations, self.Controller.distancesInLocation, self.Controller.trainData, self.Controller.trainPoints, self.Controller.levyCoeff)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()