import sys
from PyQt5 import QtWidgets, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """ Class which contains logic for a system tray interactive icon"""

    # temp icon & name
    icon = "project\\tempicon.ico"
    name = "Example tray icon"

    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon(self.icon), parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Temp Option One")
        self.setContextMenu(menu)
        self.setToolTip(self.name)
