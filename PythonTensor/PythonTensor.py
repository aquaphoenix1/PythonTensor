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

import json

class ExampleApp(QtWidgets.QMainWindow, UI.Ui_MainWindow):
    Controller = NetworkController()

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д.  в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButtonLoadFile_6.clicked.connect(self.browse_file)
        self.pushButtonConvert_7.clicked.connect(self.convert_click)
        self.pushButtonLoadFileToNeuralNetwork.clicked.connect(self.loadTraining_click)
        self.pushButtonDeserialize.clicked.connect(self.deserialize)
        self.pushButtonSerialize.clicked.connect(self.serialize)
        self.pushButtonPlotTrain.clicked.connect(self.plotTrain)
        self.pushButtonInit.clicked.connect(self.netInit)
        self.pushButtonTrain_2.clicked.connect(self.train_click)
        self.pushButtonTesting.clicked.connect(self.testing_click)
        self.textEditFilePath_6.setText('C:/Users/aqua_/source/repos/GPSConverter/GPSConverter/bin/Debug/ConvertedData/1.txtPC.csv')
        self.model = SetListModel()
        #self.listView_6.setModel(self.model)
        #self.listView_6.selectionModel().selectionChanged.connect(self.listChangedEvent)
        graphWidget = pg.PlotWidget()
        self.verticalLayoutMainNetwork.addWidget(graphWidget)
        self.sourceVisualizer = Visualizer(graphWidget)

        #graphWidget = pg.PlotWidget()
        self.listView.setModel(self.model)
        #self.clusterVisualizer = Visualizer(graphWidget);

    def netInit(self):
        window = int(self.textEditWindow.toPlainText())
        self.Controller.Network.init(window, self.Controller.getFeaturesCount(), self.Controller.getLocationsCount())


    def browse_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'C:/Users/aqua_/source/repos/GPSConverter/GPSConverter/bin/Debug/ConvertedData/')[0]
        self.textEditFilePath_6.setText(fname)

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
                        num = KAISTParser.parse(content, num, plotData, points, arr)

                    data.append(arr)

        else:
            return

        locations = LocationsCalculator().calculate(points)        

        self.plot(data)
        self.plotLocations(locations)
        self.Controller.setTrainData(data, locations)
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

        self.plot(data)
        self.plotLocations(locations)
        self.Controller.setTrainData(data, locations)
        LocationsCalculator.locations = locations
        #self.fillTable(plotData)

    def testing_click(self):
        count = int(self.textEditTestingCount.toPlainText())
        startPoints = self.textEditTestingStart.toPlainText().split('\n')
        data = []
        for i in range(len(startPoints)):
            if not startPoints[i] == '':
                point = startPoints[i].split(' ')
                for k in range(len(point)):
                    point[k] = float(point[k])
                #a = Controller.Network.normalize([point])
                data.append(point)

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
        #d = QtWidgets.QFileDialog.getOpenFileNames(self, 'Open file', 'C:/Users/aqua_/source/repos/PythonTensor/PythonTensor/Data/KAIST')

        #for i in d[0]:
            name = self.textEditFilePath_6.toPlainText() #i
            f = open(name, 'r')
            content = f.read()
            f.close()
            if not content.split('\n')[0].find('\t') == -1:
                KAISTSplitter().Split(content, name)
            else:
                Splitter().Split(content, name)

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
        self.Controller.plotCharacteristics([])

    def train_click(self):
        trainPercent = int(self.textEditTrainPercent_2.toPlainText())
        self.Controller.Network.train(self.Controller.getTrainData(), trainPercent, self.Controller.minTime, self.Controller.maxTime, self.Controller.minPauseTime, self.Controller.maxPauseTime)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()