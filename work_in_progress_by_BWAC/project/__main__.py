from PyQt5.QtWidgets import QMainWindow, QApplication

import sys

#from project import ClipboardManager
#from .utils import CONSTANTS

#also these errored

from PyQt5 import QtCore, QtWidgets


# print("hello %s" % sys.argv[1])
# print(add(2, 2))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Enter name' #enter the name of the window (i dont know why the CONSTANTS['NAME'] is for)
        # self.left = 10
        # self.top = 10
        # self.width = 640
        # self.height = 480
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.setupUi()
        self.show()

    def setupUi(self):
        # MainWindow.setObjectName("MainWindow")

        self.setFixedSize(631, 462) 
        '''makes it non resize able, change to self.resize(640, 480) for it not to be
        it is 631, 761 because it looks nice
        '''

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.Add = QtWidgets.QPushButton(self.centralwidget)
        self.Add.setGeometry(QtCore.QRect(0, 3, 51, 20))
        self.Add.setObjectName("Add")

        self.Remove = QtWidgets.QPushButton(self.centralwidget)
        self.Remove.setGeometry(QtCore.QRect(50, 3, 51, 20))
        self.Remove.setObjectName("Remove")

        self.Edit = QtWidgets.QPushButton(self.centralwidget)
        self.Edit.setGeometry(QtCore.QRect(100, 3, 51, 20))
        self.Edit.setObjectName("Edit")

        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(0, 30, 631, 411))
        self.treeWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuPlugins = QtWidgets.QMenu(self.menubar)
        self.menuPlugins.setObjectName("menuPlugins")

        self.menuItem = QtWidgets.QMenu(self.menubar)
        self.menuItem.setObjectName("menuItem")

        self.setMenuBar(self.menubar)
        
        #self.statusbar = QtWidgets.QStatusBar(self)
        #self.statusbar.setObjectName("statusbar")
        #self.setStatusBar(self.statusbar)

        #if you want the status bar back, set the size of the window to 640, 280

        self.actionAdd = QtWidgets.QAction(self)
        self.actionAdd.setObjectName("actionAdd")
        self.actionDelete = QtWidgets.QAction(self)
        self.actionDelete.setObjectName("actionDelete")
        self.action_todo = QtWidgets.QAction(self)
        self.action_todo.setObjectName("action_todo")
        self.actionSettings = QtWidgets.QAction(self)
        self.actionSettings.setObjectName("actionSettings")
        self.actionAdd_2 = QtWidgets.QAction(self)
        self.actionAdd_2.setObjectName("actionAdd_2")
        self.actionRemove = QtWidgets.QAction(self)
        self.actionRemove.setObjectName("actionRemove")
        self.menuFile.addAction(self.actionSettings)
        self.menuPlugins.addAction(self.action_todo)
        self.menuItem.addAction(self.actionAdd_2)
        self.menuItem.addAction(self.actionRemove)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPlugins.menuAction())
        self.menubar.addAction(self.menuItem.menuAction())

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        # MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Add.setText(_translate("MainWindow", "Add"))
        self.Remove.setText(_translate("MainWindow", "Remove"))
        self.Edit.setText(_translate("MainWindow", "Edit"))
        self.treeWidget.headerItem()\
            .setText(0, _translate("MainWindow", "Items:"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0)\
            .setText(0, _translate("MainWindow", "Test copy"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuPlugins.setTitle(_translate("MainWindow", "Plugins"))
        self.menuItem.setTitle(_translate("MainWindow", "Items"))
        self.actionAdd.setText(_translate("MainWindow", "Add"))
        self.actionDelete.setText(_translate("MainWindow", "Delete"))
        self.action_todo.setText(_translate("MainWindow", "Install #todo"))
        self.actionSettings.setText(_translate("MainWindow", "Settings #todo"))
        self.actionAdd_2.setText(_translate("MainWindow", "Add #todo"))
        self.actionRemove.setText(_translate("MainWindow", "Remove #todo"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # label = QLabel('Hello World!')
    # label.show()

    #clipboard_mgr = ClipboardManager.ClipboardManager()
    main_window = MainWindow()

    sys.exit(app.exec_())
