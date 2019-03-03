import operator

from PySide2.QtCore import SIGNAL, QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    """
    Class containing the Table Model to be loaded into the QTableView

    Attributes:
        table_data (list of tuple of str): Data to populate the table.
            Each tuple is a row, with each item in the tuple being a column in
            that row.
        header (tuple of str): The header items Title, Description, Deadline and
            Completed.
    """

    def __init__(self, parent, table_data, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.table_data = table_data
        self.header = header

    def rowCount(self, parent):
        return len(self.table_data)

    def columnCount(self, parent):
        return len(self.header)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.table_data[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        else:
            return None

    def sort(self, col, order):
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.table_data = sorted(self.table_data, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.table_data.reverse()
        self.emit(SIGNAL("layoutChanged()"))
