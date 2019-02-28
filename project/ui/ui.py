from PySide2.QtWidgets import QDesktopWidget, QMainWindow, qApp

from .ui_files.ui_main import Ui_MainApplication
from .add_task import AddTask


class MainApplication(QMainWindow, Ui_MainApplication):
    """
    Main Class for the Application.

    Attributes:
        windows (list of object): A list of new windows opened so they do not
            get garbage collected.
    """

    def __init__(self):
        super().__init__()
        self.init_UI()
        self.bind_buttons()
        self.windows = []
        self.count =0

    def init_UI(self):
        """
        Load the .ui-converted .py file, center the application and display it.
        """
        self.setupUi(self)
        self.center()
        self.show()

    def center(self):
        """
        Centers application to screen.
        """
        frame = self.frameGeometry()  # frame of the window
        screen_center = QDesktopWidget().availableGeometry().center()
        frame.moveCenter(screen_center)
        self.move(frame.topLeft())

    def bind_buttons(self):
        self.create_task_button.clicked.connect(self.add_task)
        #Added Edit task button
        self.edit_task_button.clicked.connect(self.edit_task)

    def add_task(self):
        """
        Create the Add Task window and append it to the list of windows.
        """
        form = AddTask()
        self.windows.append(form)

    def edit_task(self):
        pass
        #edit_task_button.setText("Press Me")

    def closeEvent(self, event):
        """
        Reimplementing the closeEvent handler to close all windows when the main
        window is closed.
        """
        qApp.quit()
