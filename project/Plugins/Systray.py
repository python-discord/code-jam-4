import sys  # noqa: F401
from PyQt5 import QtWidgets, QtGui
from project.utils import CONSTANTS


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """ Class which contains logic for a system tray interactive icon"""

    icon = CONSTANTS["ICON_LOCATION"]
    name = CONSTANTS["NAME"]

    def __init__(self, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon(self.icon), parent)
        menu = QtWidgets.QMenu(parent)
        showAction = menu.addAction("Show Clipboard")  # noqa: F841
        self.setContextMenu(menu)
        self.setToolTip(self.name)
