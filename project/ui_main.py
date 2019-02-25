import sys
from PySide2.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QWidget
)


class MainApplication(QWidget):
    """
    Main Class for the Graphics Interface.
    """

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        """
        Initializes UI.
        """

        self.center()
        self.setWindowTitle("#TODO: Application")
        self.show()

    def center(self):
        """
        Centers application to screen.
        """
        frame = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())


def start_GUI():
    """
    Starts the Graphical User Interface.
    Calls sys.exit upon closure of program.
    """
    app = QApplication(["#TODO: Application"])
    _ = MainApplication()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_GUI()
