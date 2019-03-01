import operator
from PySide2.QtCore import QAbstractTableModel, Qt, SIGNAL


class TableModel(QAbstractTableModel):
    def __init__(self, parent, data, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.data = data
        self.header = header

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        else:
            return self.data[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        else:
            return None

    def sort(self, col, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.data = sorted(self.data, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.data.reverse()
        self.emit(SIGNAL("layoutChanged()"))
