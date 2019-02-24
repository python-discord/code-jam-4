"""
.. module:: MainListView
    :synopsis: The scrollable area in the main user interface, \
    with helper functions to add or remove objects

.. moduleauthor:: TBD
"""
from PyQt5.QtWidgets import QListWidget, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

from project.ClipboardManager.ClipboardObject import TextClipboardObject


class MainListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.addItem("Sample Item")


# https://www.pythoncentral.io/pyside-pyqt-tutorial-the-qlistwidget/
# Or it can be created with the list as a parent, then automatically added to the list
# Or... https://stackoverflow.com/questions/25187444/pyqt-qlistwidget-custom-items
class TextListWidgetItem(QWidget):
    """A row in the scrollview of the actual widget."""

    def __init__(self, index: int, obj: TextClipboardObject, parent=None):
        super(TextListWidgetItem, self).__init__(parent)

        self._main_hbox_layout = QHBoxLayout()

        self._right_section = QWidget()
        self._right_vbox_layout = QVBoxLayout()

        self._text_area = QLabel()
        # self._text_area.setReadOnly(True)
        self._text_area.setText(obj.text)

        self._date_label = QLabel()
        self._date_label.setText(obj.date().strftime("%Y-%m-%d %H:%M:%S"))

        # Date should be at the bottom.
        self._right_vbox_layout.addWidget(self._text_area)
        self._right_vbox_layout.addWidget(self._date_label)

        self._right_section.setLayout(self._right_vbox_layout)
        self._right_section.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._index_label = QLabel()
        self._index_label.setText(str(index))

        self._main_hbox_layout.addWidget(self._index_label)
        self._main_hbox_layout.addWidget(self._right_section)

        self.setLayout(self._main_hbox_layout)
