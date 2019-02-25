import sys

from PySide2.QtWidgets import QApplication

from project import library
from project.widgets.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Music Player")

    library.create_db()

    window = MainWindow()
    window.setWindowTitle("Music Player")
    window.show()

    sys.exit(app.exec_())
