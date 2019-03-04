from PySide2.QtCore import QModelIndex
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate


class CurrentMediaDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        option.font.setBold(True)
        super().paint(painter, option, index)
