from PyQt5.QtWidgets import QApplication
from .gui import MinesweeperApp
from . import resources  # noqa
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MinesweeperApp()
    window.show()

    sys.exit(app.exec_())
