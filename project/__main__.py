from PyQt5.QtWidgets import QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QWidget, QListWidgetItem
from PyQt5 import QtCore, QtWidgets

import sys

from project import ClipboardManager
from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Stack import Stack
from project.Widgets.MainListWidget import MainListWidget, TextListWidgetItem
from project.SystrayManager import Systray
from .utils import CONSTANTS

# Put this in the commit message not the code @BWACpro
'''I (BWACpro) removed a lot a of comments, if i was important, uh go find a earlier commit'''

class ActionBar(QWidget):
    """ A bar which contains the controls for adding to this list of clipboard items"""
    def __init__(self):
        super().__init__()
        _horizontal_layout = QHBoxLayout(self)

        self._add_btn = QtWidgets.QPushButton("Add")
        self._add_btn.setObjectName(MainWindow.ADD_BUTTON_NAME) # can we not do this in the constructor?

        self._remove_btn = QtWidgets.QPushButton("Remove")
        self._remove_btn.setObjectName(MainWindow.REMOVE_BUTTON_NAME)

        self._edit_btn = QtWidgets.QPushButton("Edit")
        self._edit_btn.setObjectName(MainWindow.EDIT_BUTTON_NAME)

        _horizontal_layout.addWidget(self._add_btn)
        _horizontal_layout.addWidget(self._remove_btn)
        _horizontal_layout.addWidget(self._edit_btn)
        _horizontal_layout.addStretch(1)


class MainWindow(QMainWindow):
    """ MainWindow """
    # strange constants:
    CENTRAL_WIDGET_NAME = 'central_widget'
    ADD_BUTTON_NAME = 'add_btn'
    REMOVE_BUTTON_NAME = 'remove_btn'
    EDIT_BUTTON_NAME = 'edit_btn'

    # please label what these are / relate to:
    num_of_objects = 0
    items = []

    def __init__(self, clipboard_manager: ClipboardManager):
        """ Initialises new MainWindow class """
        super().__init__()

        self._central_widget_layout = QVBoxLayout()
        self._central_widget = QtWidgets.QWidget(self)
        self._clipboard_manager = clipboard_mgr

        self._clipboard_manager.bind_clipboard_state_callback(self._render_clipboard_stack)
        self._init_ui()

    def _init_ui(self):
        """ Creates UI """

        self.setWindowTitle(CONSTANTS['NAME']) # can we not pass this as a argument in the super of the constructor?

        # No idea what all these widgets are. Please clarify and comment around BWAC?
        self._central_widget.setObjectName(MainWindow.CENTRAL_WIDGET_NAME)

        self._action_bar = ActionBar()
        self._central_widget_layout.addWidget(self._action_bar)

        self._main_list_widget = MainListWidget()
        self._central_widget_layout.addWidget(self._main_list_widget)

        # menu bar has no members?
        self.menubar = self.menuBar()
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.actionSettings = QtWidgets.QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        # self.actionAdd_2 = QtWidgets.QAction(self)
        # self.actionAdd_2.setObjectName("actionAdd_2")
        # self.actionRemove = QtWidgets.QAction(self)
        # self.actionRemove.setObjectName("actionRemove")
        self.menuFile.addAction(self.actionSettings)
        # self.menuPlugins.addAction(self.action_todo)
        # self.menuItem.addAction(self.actionAdd_2)
        # self.menuItem.addAction(self.actionRemove)
        self.menubar.addAction(self.menuFile.menuAction())

        self._central_widget.setLayout(self._central_widget_layout)
        self.setCentralWidget(self._central_widget)

        self.retranslateUi()

        # https://stackoverflow.com/questions/2462401/problem-in-understanding-connectslotsbyname-in-pyqt
        # Better to use new-style decorator @QtCore.pyqtSlot()
        # QtCore.QMetaObject.connectSlotsByName(self)

        self.show()

    # temp?
    def retranslateUi(self):
        """ @transfusion What does this do?"""

        _translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self._add_btn.setText(_translate("MainWindow", "Add"))
        # self._remove_btn.setText(_translate("MainWindow", "Remove"))
        # self._edit_btn.setText(_translate("MainWindow", "Edit"))
        # self.treeWidget.headerItem() \
        #     .setText(0, _translate("MainWindow", "Items:"))
        # __sortingEnabled = self.treeWidget.isSortingEnabled()
        # self.treeWidget.setSortingEnabled(False)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        # self.menuPlugins.setTitle(_translate("MainWindow", "Plugins"))
        # self.menuItem.setTitle(_translate("MainWindow", "Items"))
        # self.actionAdd.setText(_translate("MainWindow", "Add"))
        # self.actionDelete.setText(_translate("MainWindow", "Delete"))
        # self.action_todo.setText(_translate("MainWindow", "Install #todo"))
        # self.actionSettings.setText(_translate("MainWindow", "Settings #todo"))
        # self.actionAdd_2.setText(_translate("MainWindow", "Add #todo"))
        # self.actionRemove.setText(_translate("MainWindow", "Remove #todo"))

    def _render_clipboard_stack(self, clipboard_stack: Stack):
        """ Renders the clipboard stack. no idea??"""
        self._main_list_widget.clear()
        for (idx, clipboard_object) in enumerate(clipboard_stack.items()):
            if isinstance(clipboard_object, TextClipboardObject):
                _item = QListWidgetItem(self._main_list_widget)
                _custom_item = TextListWidgetItem(idx, clipboard_object)
                _item.setSizeHint(_custom_item.sizeHint())

                self._main_list_widget.addItem(_item)
                self._main_list_widget.setItemWidget(_item, _custom_item)
    
    def closeEvent(self, event):
        """ Fires on window close"""
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    clipboard_mgr = ClipboardManager.ClipboardManager()
    main_window = MainWindow(clipboard_mgr)

    # Creates and starts systray icon
    # systray = Systray.systray(app.quit)
    # systray.start()
    # app.aboutToQuit.connect(systray.close)

    sys.exit(app.exec_())
