# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:/Users/aqua_/Desktop/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1112, 618)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMaximumSize(QtCore.QSize(999999, 999999))
        self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.fileTab = QtWidgets.QWidget()
        self.fileTab.setObjectName("fileTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.fileTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxFiles = QtWidgets.QGroupBox(self.fileTab)
        self.groupBoxFiles.setTitle("")
        self.groupBoxFiles.setObjectName("groupBoxFiles")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxFiles)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.groupBoxFiles)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalGroupBoxWindow = QtWidgets.QGroupBox(self.groupBox)
        self.verticalGroupBoxWindow.setMaximumSize(QtCore.QSize(16777215, 50))
        self.verticalGroupBoxWindow.setObjectName("verticalGroupBoxWindow")
        self.windowLayeout = QtWidgets.QHBoxLayout(self.verticalGroupBoxWindow)
        self.windowLayeout.setObjectName("windowLayeout")
        self.labelWindow = QtWidgets.QLabel(self.verticalGroupBoxWindow)
        self.labelWindow.setObjectName("labelWindow")
        self.windowLayeout.addWidget(self.labelWindow)
        self.textBrowserWindow = QtWidgets.QTextBrowser(self.verticalGroupBoxWindow)
        self.textBrowserWindow.setMaximumSize(QtCore.QSize(16777215, 25))
        self.textBrowserWindow.setObjectName("textBrowserWindow")
        self.windowLayeout.addWidget(self.textBrowserWindow)
        self.verticalLayout.addWidget(self.verticalGroupBoxWindow)
        self.pushButtonConvert = QtWidgets.QPushButton(self.groupBox)
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        self.verticalLayout.addWidget(self.pushButtonConvert)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.pushButtonSerialize = QtWidgets.QPushButton(self.groupBoxFiles)
        self.pushButtonSerialize.setObjectName("pushButtonSerialize")
        self.horizontalLayout_2.addWidget(self.pushButtonSerialize)
        self.pushButtonDeserialize = QtWidgets.QPushButton(self.groupBoxFiles)
        self.pushButtonDeserialize.setObjectName("pushButtonDeserialize")
        self.horizontalLayout_2.addWidget(self.pushButtonDeserialize)
        self.pushButtonPlotTrain = QtWidgets.QPushButton(self.groupBoxFiles)
        self.pushButtonPlotTrain.setObjectName("pushButtonPlotTrain")
        self.horizontalLayout_2.addWidget(self.pushButtonPlotTrain)
        self.pushButtonPlotNewWindow = QtWidgets.QPushButton(self.groupBoxFiles)
        self.pushButtonPlotNewWindow.setObjectName("pushButtonPlotNewWindow")
        self.horizontalLayout_2.addWidget(self.pushButtonPlotNewWindow)
        self.gridLayout_2.addWidget(self.groupBoxFiles, 1, 0, 1, 1)
        self.tabWidget.addTab(self.fileTab, "")
        self.visualizeTab = QtWidgets.QWidget()
        self.visualizeTab.setObjectName("visualizeTab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.visualizeTab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayoutVisWIthTabs = QtWidgets.QVBoxLayout()
        self.verticalLayoutVisWIthTabs.setObjectName("verticalLayoutVisWIthTabs")
        self.tabWidgetGraph = QtWidgets.QTabWidget(self.visualizeTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidgetGraph.sizePolicy().hasHeightForWidth())
        self.tabWidgetGraph.setSizePolicy(sizePolicy)
        self.tabWidgetGraph.setMaximumSize(QtCore.QSize(16777215, 20))
        self.tabWidgetGraph.setObjectName("tabWidgetGraph")
        self.tabLengthInLocations = QtWidgets.QWidget()
        self.tabLengthInLocations.setObjectName("tabLengthInLocations")
        self.tabWidgetGraph.addTab(self.tabLengthInLocations, "")
        self.tabTracesTime = QtWidgets.QWidget()
        self.tabTracesTime.setObjectName("tabTracesTime")
        self.tabWidgetGraph.addTab(self.tabTracesTime, "")
        self.tabJumpLength = QtWidgets.QWidget()
        self.tabJumpLength.setObjectName("tabJumpLength")
        self.tabWidgetGraph.addTab(self.tabJumpLength, "")
        self.tabPauseTimes = QtWidgets.QWidget()
        self.tabPauseTimes.setObjectName("tabPauseTimes")
        self.tabWidgetGraph.addTab(self.tabPauseTimes, "")
        self.tabLocationsCount = QtWidgets.QWidget()
        self.tabLocationsCount.setObjectName("tabLocationsCount")
        self.tabWidgetGraph.addTab(self.tabLocationsCount, "")
        self.tabUnique = QtWidgets.QWidget()
        self.tabUnique.setObjectName("tabUnique")
        self.tabWidgetGraph.addTab(self.tabUnique, "")
        self.verticalLayoutVisWIthTabs.addWidget(self.tabWidgetGraph)
        self.verticalWidget = QtWidgets.QWidget(self.visualizeTab)
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayoutVisWIthTabs.addWidget(self.verticalWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayoutVisWIthTabs)
        self.verticalWidget_2 = QtWidgets.QWidget(self.visualizeTab)
        self.verticalWidget_2.setMaximumSize(QtCore.QSize(210, 16777215))
        self.verticalWidget_2.setObjectName("verticalWidget_2")
        self.verticalLayoutVisBtns = QtWidgets.QVBoxLayout(self.verticalWidget_2)
        self.verticalLayoutVisBtns.setObjectName("verticalLayoutVisBtns")
        self.checkBoxPlotTrained = QtWidgets.QCheckBox(self.verticalWidget_2)
        self.checkBoxPlotTrained.setChecked(True)
        self.checkBoxPlotTrained.setObjectName("checkBoxPlotTrained")
        self.verticalLayoutVisBtns.addWidget(self.checkBoxPlotTrained)
        self.pushButtonAddGraph = QtWidgets.QPushButton(self.verticalWidget_2)
        self.pushButtonAddGraph.setObjectName("pushButtonAddGraph")
        self.verticalLayoutVisBtns.addWidget(self.pushButtonAddGraph)
        self.pushButtonAddChecking = QtWidgets.QPushButton(self.verticalWidget_2)
        self.pushButtonAddChecking.setObjectName("pushButtonAddChecking")
        self.verticalLayoutVisBtns.addWidget(self.pushButtonAddChecking)
        self.pushButtonClearGraph = QtWidgets.QPushButton(self.verticalWidget_2)
        self.pushButtonClearGraph.setObjectName("pushButtonClearGraph")
        self.verticalLayoutVisBtns.addWidget(self.pushButtonClearGraph)
        self.horizontalLayout_3.addWidget(self.verticalWidget_2)
        self.tabWidget.addTab(self.visualizeTab, "")
        self.tabNeural = QtWidgets.QWidget()
        self.tabNeural.setObjectName("tabNeural")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabNeural)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBoxNetInit = QtWidgets.QGroupBox(self.tabNeural)
        self.groupBoxNetInit.setObjectName("groupBoxNetInit")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBoxNetInit)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButtonInit = QtWidgets.QPushButton(self.groupBoxNetInit)
        self.pushButtonInit.setObjectName("pushButtonInit")
        self.verticalLayout_3.addWidget(self.pushButtonInit)
        self.pushButtonNetSerialize = QtWidgets.QPushButton(self.groupBoxNetInit)
        self.pushButtonNetSerialize.setObjectName("pushButtonNetSerialize")
        self.verticalLayout_3.addWidget(self.pushButtonNetSerialize)
        self.pushButtonNetDeserialize = QtWidgets.QPushButton(self.groupBoxNetInit)
        self.pushButtonNetDeserialize.setObjectName("pushButtonNetDeserialize")
        self.verticalLayout_3.addWidget(self.pushButtonNetDeserialize)
        self.verticalLayout_2.addWidget(self.groupBoxNetInit)
        self.groupBoxNetTrain = QtWidgets.QGroupBox(self.tabNeural)
        self.groupBoxNetTrain.setObjectName("groupBoxNetTrain")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBoxNetTrain)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushButtonTrain = QtWidgets.QPushButton(self.groupBoxNetTrain)
        self.pushButtonTrain.setObjectName("pushButtonTrain")
        self.verticalLayout_4.addWidget(self.pushButtonTrain)
        self.verticalLayout_2.addWidget(self.groupBoxNetTrain)
        self.groupBoxNetGeneration = QtWidgets.QGroupBox(self.tabNeural)
        self.groupBoxNetGeneration.setObjectName("groupBoxNetGeneration")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBoxNetGeneration)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pushButtonGenerate = QtWidgets.QPushButton(self.groupBoxNetGeneration)
        self.pushButtonGenerate.setObjectName("pushButtonGenerate")
        self.verticalLayout_5.addWidget(self.pushButtonGenerate)
        self.verticalLayout_2.addWidget(self.groupBoxNetGeneration)
        self.tabWidget.addTab(self.tabNeural, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidgetGraph.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelWindow.setText(_translate("MainWindow", "Размер окна"))
        self.textBrowserWindow.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">5</p></body></html>"))
        self.pushButtonConvert.setText(_translate("MainWindow", "Преобразовать"))
        self.pushButtonSerialize.setText(_translate("MainWindow", "Сериализация"))
        self.pushButtonDeserialize.setText(_translate("MainWindow", "Десериализация"))
        self.pushButtonPlotTrain.setText(_translate("MainWindow", "Построить обучающую выборку"))
        self.pushButtonPlotNewWindow.setText(_translate("MainWindow", "Построить в новом окне"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.fileTab), _translate("MainWindow", "Работа с файлами"))
        self.tabWidgetGraph.setTabText(self.tabWidgetGraph.indexOf(self.tabLengthInLocations), _translate("MainWindow", "Длины трасс в локациях"))
        self.tabWidgetGraph.setTabText(self.tabWidgetGraph.indexOf(self.tabTracesTime), _translate("MainWindow", "Время трасс"))
        self.tabWidgetGraph.setTabText(self.tabWidgetGraph.indexOf(self.tabJumpLength), _translate("MainWindow", "Длина прыжков"))
        self.tabWidgetGraph.setTabText(self.tabWidgetGraph.indexOf(self.tabPauseTimes), _translate("MainWindow", "Время пауз"))
        self.tabWidgetGraph.setTabText(self.tabWidgetGraph.indexOf(self.tabLocationsCount), _translate("MainWindow", "Количество посещений локаций"))
        self.tabWidgetGraph.setTabText(self.tabWidgetGraph.indexOf(self.tabUnique), _translate("MainWindow", "Уникальные локации"))
        self.checkBoxPlotTrained.setText(_translate("MainWindow", "Отображать обучающую выборку"))
        self.pushButtonAddGraph.setText(_translate("MainWindow", "Добавить график"))
        self.pushButtonAddChecking.setText(_translate("MainWindow", "Добавить проверочную"))
        self.pushButtonClearGraph.setText(_translate("MainWindow", "Очистить график"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.visualizeTab), _translate("MainWindow", "Визуализация"))
        self.groupBoxNetInit.setTitle(_translate("MainWindow", "Инициализация"))
        self.pushButtonInit.setText(_translate("MainWindow", "Инициализация"))
        self.pushButtonNetSerialize.setText(_translate("MainWindow", "Сериализация"))
        self.pushButtonNetDeserialize.setText(_translate("MainWindow", "Десериализация"))
        self.groupBoxNetTrain.setTitle(_translate("MainWindow", "Обучение"))
        self.pushButtonTrain.setText(_translate("MainWindow", "Обучить"))
        self.groupBoxNetGeneration.setTitle(_translate("MainWindow", "Генерация"))
        self.pushButtonGenerate.setText(_translate("MainWindow", "Генерация"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNeural), _translate("MainWindow", "Работа с сетью"))
