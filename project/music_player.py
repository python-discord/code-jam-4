import sys

from PySide2.QtWidgets import QApplication

from project.widgets.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Music Player")

    window = MainWindow()
    window.setWindowTitle("Music Player")
    window.show()

    sys.exit(app.exec_())
