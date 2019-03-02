from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from .gui import MinesweeperApp
from . import resources  # noqa
import sys

if __name__ == '__main__':
    # For high DPI displays
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    window = MinesweeperApp()
    window.show()

    sys.exit(app.exec_())
