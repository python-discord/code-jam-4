import sys
from PySide2.QtWidgets import QApplication
from .ui.ui import MainApplication


def main():
    app = QApplication(sys.argv)
    _ = MainApplication()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
