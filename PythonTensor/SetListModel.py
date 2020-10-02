from PyQt5 import QtCore
from PyQt5 import QtGui

class SetListModel(QtCore.QAbstractListModel):
    def __init__(self, data=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__data = data

    def rowCount(self, parent):
        return len(self.__data)

    def data(self, index, role):
        if role == QtCore.Qt.EditRole:
            return self.__data[index.row()]

        if role == QtCore.Qt.ToolTipRole:
            return self.__data[index].points

        if role == QtCore.Qt.DecorationRole:
            pixmax = QtGui.QPixmap(26, 26)
            pixmax.fill(QtGui.QColor('black'))
            return QtGui.QIcon(pixmax)

        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.__data[row]
            return value.number

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            data_value = value
            self.__data[row][0] = data_value
            self.dataChanged.emit(index, index)
            return True

    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


    def insertRows(self, position, rows, data, parent = QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.__data.insert(position, data[i])
        self.endInsertRows()
        return True

    def getData(self, index):
        return self.data(index, QtCore.Qt.ToolTipRole)

    def deleteRows(self, position, parent = QtCore.QModelIndex()):
        rows = len(self.__data)
        self.beginRemoveRows(parent, position, position + rows - 1)
        for i in range(rows):
            self.__data.remove(self.__data[position])
        self.endRemoveRows()
        return True
