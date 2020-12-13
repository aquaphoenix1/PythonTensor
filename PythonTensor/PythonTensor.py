import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import UI  # Это наш конвертированный файл дизайна
from Splitter.Splitter import Splitter
from Clusterizer.Cluster import Cluster
from SetListModel import SetListModel
import pyqtgraph as pg
from PyQt5 import QtCore
from Visualizer import Visualizer
from network.Network import Network

class ExampleApp(QtWidgets.QMainWindow, UI.Ui_MainWindow):
    Splitter = Splitter();

    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButtonLoadFile_6.clicked.connect(self.browse_file)
        self.pushButtonConvert_6.clicked.connect(self.convert_click)
        self.textEditFilePath_6.setText('C:/Users/aqua_/source/repos/GPSConverter/GPSConverter/bin/Debug/ConvertedData/1.txtPC.csv')
        self.model = SetListModel()
        self.listView_6.setModel(self.model)
        self.listView_6.selectionModel().selectionChanged.connect(self.listChangedEvent)
        graphWidget = pg.PlotWidget()
        self.horizontalLayoutMain.addWidget(graphWidget)
        self.sourceVisualizer = Visualizer(graphWidget)

        graphWidget = pg.PlotWidget()
        self.horizontalLayoutMain.addWidget(graphWidget)
        self.clusterVisualizer = Visualizer(graphWidget);

        self.pushButtonClusterize.clicked.connect(self.clusterize_click);


    def browse_file(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        self.textEditFilePath_6.setText(fname)

    def convert_click(self):
        name = self.textEditFilePath_6.toPlainText()
        f = open(name, 'r')
        content = f.read()
        f.close()
        content = self.Splitter.Split(content)
        self.clearList()
        self.model.insertRows(0, len(content), content)


    def clearList(self):
        self.model.deleteRows(0)

    currentData = None

    def listChangedEvent(self, prev, current):
        data = self.model.getData(self.listView_6.selectedIndexes()[0].data())
        x = []
        y = []
        for i in range(len(data)):
            x.append(data[i].latitude)
            y.append(data[i].longitude)

        self.currentData = data;

        self.sourceVisualizer.clear()
        self.sourceVisualizer.plot(x, y)

        self.labelSource.setText(str(len(x)))


        # Network().loadDataset(data)

    def clusterize_click(self):
        data = Cluster().clusterizeData(self.currentData);

        x = []
        y = []
        for i in range(len(data)):
            x.append(data[i].latitude)
            y.append(data[i].longitude)

        self.clusterVisualizer.clear()
        self.clusterVisualizer.plot(x, y)

        self.labelClusterize.setText(str(len(x)))


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()