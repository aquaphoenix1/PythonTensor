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
        MainWindow.resize(1084, 592)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1071, 581))
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
        self.pushButtonConvert_6 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonConvert_6.sizePolicy().hasHeightForWidth())
        self.pushButtonConvert_6.setSizePolicy(sizePolicy)
        self.pushButtonConvert_6.setObjectName("pushButtonConvert_6")
        self.horizontalLayout_7.addWidget(self.pushButtonConvert_6)
        self.radioButtonDay_6 = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.radioButtonDay_6.setChecked(True)
        self.radioButtonDay_6.setObjectName("radioButtonDay_6")
        self.horizontalLayout_7.addWidget(self.radioButtonDay_6)
        self.verticalLayoutMain_6.addLayout(self.horizontalLayout_7)
        self.listView_6 = QtWidgets.QListView(self.horizontalLayoutWidget)
        self.listView_6.setObjectName("listView_6")
        self.verticalLayoutMain_6.addWidget(self.listView_6)
        self.horizontalLayoutMain.addLayout(self.verticalLayoutMain_6)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonLoadFile_6.setText(_translate("MainWindow", "Загрузить файл"))
        self.pushButtonConvert_6.setText(_translate("MainWindow", "Преобразовать"))
        self.radioButtonDay_6.setText(_translate("MainWindow", "День"))