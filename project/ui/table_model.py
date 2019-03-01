import operator
from PySide2.QtCore import QAbstractTableModel, Qt, SIGNAL


class TableModel(QAbstractTableModel):
    def __init__(self, parent, data, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.data = data
        print(self.data)
        print(self.data[0][0])
        self.header = header
        print(self.header)

    def rowCount(self, parent):  #rowCount(self, parent)
        return len(self.data)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        print("data")
        if not index.isValid() or role != Qt.DisplayRole:
            print ("Enter Error!")
            return None
        else:
            print(index.role())
            return self.data[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        print("HeaderData")
        #This is the Error!!!
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            print(self.header[col])
            return self.header[col]
        else:
            print("Nothin")
            return None

    def sort(self, col, order):
        print("sort")
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.data = sorted(self.data, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.data.reverse()
        self.emit(SIGNAL("layoutChanged()"))
