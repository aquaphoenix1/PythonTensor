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
        MainWindow.resize(1080, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 0, 1081, 591))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabFiles = QtWidgets.QWidget()
        self.tabFiles.setObjectName("tabFiles")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tabFiles)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1071, 561))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutMain = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutMain.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutMain.setObjectName("horizontalLayoutMain")
        self.verticalLayoutMain_6 = QtWidgets.QVBoxLayout()
        self.verticalLayoutMain_6.setObjectName("verticalLayoutMain_6")
        self.horizontalLayoutLoadFile_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutLoadFile_6.setObjectName("horizontalLayoutLoadFile_6")
        self.pushButtonLoadFile_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLoadFile_6.sizePolicy().hasHeightForWidth())
        self.pushButtonLoadFile_6.setSizePolicy(sizePolicy)
        self.pushButtonLoadFile_6.setObjectName("pushButtonLoadFile_6")
        self.horizontalLayoutLoadFile_6.addWidget(self.pushButtonLoadFile_6)
        self.textEditFilePath_6 = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditFilePath_6.sizePolicy().hasHeightForWidth())
        self.textEditFilePath_6.setSizePolicy(sizePolicy)
        self.textEditFilePath_6.setMaximumSize(QtCore.QSize(16777215, 23))
        self.textEditFilePath_6.setObjectName("textEditFilePath_6")
        self.horizontalLayoutLoadFile_6.addWidget(self.textEditFilePath_6)
        self.verticalLayoutMain_6.addLayout(self.horizontalLayoutLoadFile_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pushButtonConvert_7 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonConvert_7.sizePolicy().hasHeightForWidth())
        self.pushButtonConvert_7.setSizePolicy(sizePolicy)
        self.pushButtonConvert_7.setObjectName("pushButtonConvert_7")
        self.horizontalLayout_7.addWidget(self.pushButtonConvert_7)
        self.pushButtonLoadFileToNeuralNetwork = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLoadFileToNeuralNetwork.sizePolicy().hasHeightForWidth())
        self.pushButtonLoadFileToNeuralNetwork.setSizePolicy(sizePolicy)
        self.pushButtonLoadFileToNeuralNetwork.setObjectName("pushButtonLoadFileToNeuralNetwork")
        self.horizontalLayout_7.addWidget(self.pushButtonLoadFileToNeuralNetwork)
        self.verticalLayoutMain_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayoutMain.addLayout(self.verticalLayoutMain_6)
        self.tabWidget.addTab(self.tabFiles, "")
        self.tabVisualize = QtWidgets.QWidget()
        self.tabVisualize.setObjectName("tabVisualize")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.tabVisualize)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 1051, 551))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutList = QtWidgets.QVBoxLayout()
        self.verticalLayoutList.setObjectName("verticalLayoutList")
        self.listView = QtWidgets.QListView(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy)
        self.listView.setObjectName("listView")
        self.verticalLayoutList.addWidget(self.listView)
        self.horizontalLayout.addLayout(self.verticalLayoutList)
        self.verticalLayoutMainNetwork = QtWidgets.QVBoxLayout()
        self.verticalLayoutMainNetwork.setObjectName("verticalLayoutMainNetwork")
        self.horizontalLayout.addLayout(self.verticalLayoutMainNetwork)
        self.tabWidget.addTab(self.tabVisualize, "")
        self.tabNeural = QtWidgets.QWidget()
        self.tabNeural.setObjectName("tabNeural")
        self.groupBoxLearning = QtWidgets.QGroupBox(self.tabNeural)
        self.groupBoxLearning.setGeometry(QtCore.QRect(10, 90, 250, 81))
        self.groupBoxLearning.setMaximumSize(QtCore.QSize(250, 120))
        self.groupBoxLearning.setObjectName("groupBoxLearning")
        self.textEditTrainPercent_2 = QtWidgets.QTextEdit(self.groupBoxLearning)
        self.textEditTrainPercent_2.setGeometry(QtCore.QRect(190, 20, 51, 21))
        self.textEditTrainPercent_2.setObjectName("textEditTrainPercent_2")
        self.labelTrainPercent_2 = QtWidgets.QLabel(self.groupBoxLearning)
        self.labelTrainPercent_2.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.labelTrainPercent_2.setObjectName("labelTrainPercent_2")
        self.pushButtonTrain_2 = QtWidgets.QPushButton(self.groupBoxLearning)
        self.pushButtonTrain_2.setGeometry(QtCore.QRect(10, 50, 221, 23))
        self.pushButtonTrain_2.setObjectName("pushButtonTrain_2")
        self.groupBoxTesting = QtWidgets.QGroupBox(self.tabNeural)
        self.groupBoxTesting.setGeometry(QtCore.QRect(10, 190, 621, 171))
        self.groupBoxTesting.setMaximumSize(QtCore.QSize(700, 500))
        self.groupBoxTesting.setObjectName("groupBoxTesting")
        self.textEditTestingCount = QtWidgets.QTextEdit(self.groupBoxTesting)
        self.textEditTestingCount.setGeometry(QtCore.QRect(190, 20, 51, 21))
        self.textEditTestingCount.setObjectName("textEditTestingCount")
        self.labelTesting = QtWidgets.QLabel(self.groupBoxTesting)
        self.labelTesting.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.labelTesting.setObjectName("labelTesting")
        self.pushButtonTesting = QtWidgets.QPushButton(self.groupBoxTesting)
        self.pushButtonTesting.setGeometry(QtCore.QRect(10, 50, 221, 23))
        self.pushButtonTesting.setObjectName("pushButtonTesting")
        self.labelTestingStart = QtWidgets.QLabel(self.groupBoxTesting)
        self.labelTestingStart.setGeometry(QtCore.QRect(10, 80, 151, 16))
        self.labelTestingStart.setObjectName("labelTestingStart")
        self.textEditTestingStart = QtWidgets.QTextEdit(self.groupBoxTesting)
        self.textEditTestingStart.setGeometry(QtCore.QRect(10, 100, 601, 61))
        self.textEditTestingStart.setReadOnly(False)
        self.textEditTestingStart.setObjectName("textEditTestingStart")
        self.groupBoxInit = QtWidgets.QGroupBox(self.tabNeural)
        self.groupBoxInit.setGeometry(QtCore.QRect(10, 0, 250, 81))
        self.groupBoxInit.setMaximumSize(QtCore.QSize(250, 120))
        self.groupBoxInit.setObjectName("groupBoxInit")
        self.textEditWindow = QtWidgets.QTextEdit(self.groupBoxInit)
        self.textEditWindow.setGeometry(QtCore.QRect(190, 20, 51, 21))
        self.textEditWindow.setObjectName("textEditWindow")
        self.labelWindow = QtWidgets.QLabel(self.groupBoxInit)
        self.labelWindow.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.labelWindow.setObjectName("labelWindow")
        self.pushButtonInit = QtWidgets.QPushButton(self.groupBoxInit)
        self.pushButtonInit.setGeometry(QtCore.QRect(10, 50, 221, 23))
        self.pushButtonInit.setObjectName("pushButtonInit")
        self.tabWidget.addTab(self.tabNeural, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonLoadFile_6.setText(_translate("MainWindow", "Загрузить файл"))
        self.pushButtonConvert_7.setText(_translate("MainWindow", "Преобразовать"))
        self.pushButtonLoadFileToNeuralNetwork.setText(_translate("MainWindow", "Загрузить обучающую выборку"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFiles), _translate("MainWindow", "Работа с файлами"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVisualize), _translate("MainWindow", "Визуализация"))
        self.groupBoxLearning.setTitle(_translate("MainWindow", "Обучение"))
        self.textEditTrainPercent_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">100</p></body></html>"))
        self.labelTrainPercent_2.setText(_translate("MainWindow", "Процент выборки для обучения"))
        self.pushButtonTrain_2.setText(_translate("MainWindow", "Обучение"))
        self.groupBoxTesting.setTitle(_translate("MainWindow", "Генерация"))
        self.textEditTestingCount.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">10</p></body></html>"))
        self.labelTesting.setText(_translate("MainWindow", "Количество точек для генерации"))
        self.pushButtonTesting.setText(_translate("MainWindow", "Генерация"))
        self.labelTestingStart.setText(_translate("MainWindow", "Первоначальное положение"))
        self.textEditTestingStart.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0</p></body></html>"))
        self.groupBoxInit.setTitle(_translate("MainWindow", "Инициализация"))
        self.textEditWindow.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">3</p></body></html>"))
        self.labelWindow.setText(_translate("MainWindow", "Размер окна"))
        self.pushButtonInit.setText(_translate("MainWindow", "Инициализация"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabNeural), _translate("MainWindow", "Нейронная сеть"))
