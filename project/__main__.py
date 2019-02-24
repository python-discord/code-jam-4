from PyQt5.QtWidgets import QMainWindow, QApplication, \
    QHBoxLayout, QVBoxLayout, QWidget, QListWidgetItem

import sys

from project import ClipboardManager
from project.ClipboardManager.ClipboardObject import TextClipboardObject
from project.Stack import Stack
from project.Widgets.MainListWidget import MainListWidget, TextListWidgetItem
from .utils import CONSTANTS

from PyQt5 import QtCore, QtWidgets


# print("hello %s" % sys.argv[1])
# print(add(2, 2))

class ActionBar(QWidget):
    def __init__(self):
        super().__init__()
        _horizontal_layout = QHBoxLayout(self)

        self._add_btn = QtWidgets.QPushButton("Add")
        # self._add_btn.setGeometry(QtCore.QRect(0, 3, 51, 20))
        # self._add_btn.clicked.connect(self._add_object)
        self._add_btn.setObjectName(MainWindow.ADD_BUTTON_NAME)

        # self._add_btn.setStyleSheet("QPushButton {background-color: yellow, margin: 0}")

        self._remove_btn = QtWidgets.QPushButton("Remove")
        # self._remove_btn.setGeometry(QtCore.QRect(50, 3, 51, 20))
        # self._remove_btn.clicked.connect()
        self._remove_btn.setObjectName(MainWindow.REMOVE_BUTTON_NAME)

        self._edit_btn = QtWidgets.QPushButton("Edit")
        # self._edit_btn.setGeometry(QtCore.QRect(100, 3, 51, 20))
        self._edit_btn.setObjectName(MainWindow.EDIT_BUTTON_NAME)

        _horizontal_layout.addWidget(self._add_btn)
        _horizontal_layout.addWidget(self._remove_btn)
        _horizontal_layout.addWidget(self._edit_btn)
        _horizontal_layout.addStretch(1)


class MainWindow(QMainWindow):
    CENTRAL_WIDGET_NAME = 'central_widget'
    ADD_BUTTON_NAME = 'add_btn'
    REMOVE_BUTTON_NAME = 'remove_btn'
    EDIT_BUTTON_NAME = 'edit_btn'

    num_of_objects = 0
    items = []

    def __init__(self, clipboard_manager: ClipboardManager):
        super().__init__()

        self._central_widget_layout = QVBoxLayout()
        self._central_widget = QtWidgets.QWidget(self)
        self._clipboard_manager = clipboard_mgr

        self._clipboard_manager.bind_clipboard_state_callback(self._render_clipboard_stack)
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(CONSTANTS['NAME'])
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setupUi()
        self.show()

    def _render_clipboard_stack(self, clipboard_stack: Stack):
        self._main_list_widget.clear()
        for (idx, clipboard_object) in enumerate(clipboard_stack.items()):
            if isinstance(clipboard_object, TextClipboardObject):
                _item = QListWidgetItem(self._main_list_widget)
                _custom_item = TextListWidgetItem(idx, clipboard_object)
                _item.setSizeHint(_custom_item.sizeHint())

                self._main_list_widget.addItem(_item)
                self._main_list_widget.setItemWidget(_item, _custom_item)

    def setupUi(self):
        # MainWindow.setObjectName("MainWindow")
        # self.setFixedSize(640, 480)
        self._central_widget.setObjectName(MainWindow.CENTRAL_WIDGET_NAME)

        self._action_bar = ActionBar()
        self._central_widget_layout.addWidget(self._action_bar)

        self._main_list_widget = MainListWidget()
        self._central_widget_layout.addWidget(self._main_list_widget)
        # self._central_widget_layout.addStretch(1)

        # self.Add = QtWidgets.QPushButton(self._central_widget)
        # self.Add.setGeometry(QtCore.QRect(0, 3, 51, 20))
        # self.Add.clicked.connect(self.addObject)
        # self.Add.setObjectName("Add")

        # self.Remove = QtWidgets.QPushButton(self._central_widget)
        # self.Remove.setGeometry(QtCore.QRect(50, 3, 51, 20))
        # self.Remove.clicked.connect(self.removeObject)
        # self.Remove.setObjectName("Remove")
        #
        # self.Edit = QtWidgets.QPushButton(self._central_widget)
        # self.Edit.setGeometry(QtCore.QRect(100, 3, 51, 20))
        # self.Edit.setObjectName("Edit")

        # self.treeWidget = QtWidgets.QTreeWidget(self._central_widget)
        # self.treeWidget.setGeometry(QtCore.QRect(0, 30, 631, 411))
        # self.treeWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.treeWidget.setObjectName("treeWidget")

        self.menubar = self.menuBar()
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        # self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        # self.menuPlugins = QtWidgets.QMenu(self.menubar)
        # self.menuPlugins.setObjectName("menuPlugins")
        # self.menuItem = QtWidgets.QMenu(self.menubar)
        # self.menuItem.setObjectName("menuItem")
        # self.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(self)
        # self.statusbar.setObjectName("statusbar")
        # self.setStatusBar(self.statusbar)
        # self.actionAdd = QtWidgets.QAction(self)
        # self.actionAdd.setObjectName("actionAdd")
        # self.actionDelete = QtWidgets.QAction(self)
        # self.actionDelete.setObjectName("actionDelete")
        # self.action_todo = QtWidgets.QAction(self)
        # self.action_todo.setObjectName("action_todo")
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
        # self.menubar.addAction(self.menuPlugins.menuAction())
        # self.menubar.addAction(self.menuItem.menuAction())

        self._central_widget.setLayout(self._central_widget_layout)
        self.setCentralWidget(self._central_widget)

        self.retranslateUi()

        # https://stackoverflow.com/questions/2462401/problem-in-understanding-connectslotsbyname-in-pyqt
        # Better to use new-style decorator @QtCore.pyqtSlot()
        # QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
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

    # def _add_object(self):
    #     exec('item_' + str(self.num_of_objects) + ' = QtWidgets.QTreeWidgetItem(self.treeWidget)')
    #     exec('item_' + str(self.num_of_objects) + '.setText(0, "Untitled")')
    #     self.num_of_objects + 1
    # def removeObject(self):
    #     # TODO make it remove instead of add
    #
    #     if self.items == []:
    #         return
    #
    #     exec('item_' + str(self.num_of_objects) + ' = QtWidgets.QTreeWidgetItem(self.treeWidget)')
    #     exec('item_' + str(self.num_of_objects) + '.setText(0, "Untitled")')
    #
    #     self.num_of_objects + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # label = QLabel('Hello World!')
    # label.show()

    clipboard_mgr = ClipboardManager.ClipboardManager()
    main_window = MainWindow(clipboard_mgr)

    sys.exit(app.exec_())
