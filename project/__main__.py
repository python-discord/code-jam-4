from PyQt5.QtWidgets import QApplication
from .gui import Minesweeper
from . import resources
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Minesweeper(width=16, height=16)
    window.show()

    print(resources)
    sys.exit(app.exec_())
