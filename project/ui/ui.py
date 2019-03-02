from PySide2.QtWidgets import QDesktopWidget, QMainWindow, qApp
from PySide2.QtCore import QTimer

from .ui_files.ui_main import Ui_MainApplication
from .add_task import AddTask
from .datacomm import DataComm
from .table_model import TableModel


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
        self.datacomm = DataComm()
        self.table_model = TableModel(
            self, self.datacomm.tup, self.datacomm.header
        )
        self.update_table()
        timer = QTimer(self)
        timer.timeout.connect(self.update_table)
        timer.start()

    def init_UI(self):
        """
        Load the .ui-converted .py file, center the application and display it.
        """
        self.setupUi(self)
        self.resize(1200, 600)

        self.task_table.horizontalHeader().setStretchLastSection(True)

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
        self.remove_task_button.clicked.connect(self.remove_task)
        self.edit_task_button.clicked.connect(self.edit_task)

    def add_task(self):
        """
        Create the Add Task window and append it to the list of windows.
        """
        form = AddTask(self.datacomm)
        self.windows.append(form)

    def remove_task(self):
        self.datacomm.delete_task()

    def edit_task(self):
        pass
        #edit_task_button.setText("Press Me")

    def update_table(self):
        self.table_model.table_data = self.datacomm.update()
        self.task_table.setModel(self.table_model)
        self.task_table.setSortingEnabled(True)
        self.task_table.resizeColumnsToContents()

    def closeEvent(self, event):
        """
        Reimplementing the closeEvent handler to close all windows when the main
        window is closed.
        """
        qApp.quit()
