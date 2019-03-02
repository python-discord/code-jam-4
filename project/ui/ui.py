from PySide2.QtCore import QTimer
from PySide2.QtWidgets import (QAbstractItemView, QDesktopWidget, QHeaderView,
                               QMainWindow, qApp)
from .add_task import AddTask
from .datacomm import DataComm
from .table_model import TableModel
from .edit_task import MyWidget
from .ui_files.ui_main import Ui_MainApplication


class MainApplication(QMainWindow, Ui_MainApplication):
    """
    Main Class for the Application.

    Attributes:
        windows (list of object): A list of new windows opened so they do not
            get garbage collected.
        datacomm (object): The Data Communication object used to update the table
            model and communicate with the file writing class.
        table_model (object): The table model used to load into the QTableView.
        timer (object): The QTimer object used to continuously update the table.
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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_table)
        self.timer.start()

    def init_UI(self):
        """
        Load the .ui-converted .py file, center the application and display it.
        """
        self.setupUi(self)
        self.resize(1200, 600)

        # stretch the header to get equally sized columns
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # modify selection behavior to select the entire row instead of an item
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)

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
        """
        Binds the buttons to their respective functions
        """
        self.create_task_button.clicked.connect(self.add_task)
        self.remove_task_button.clicked.connect(self.remove_task)
        self.edit_task_button.clicked.connect(self.edit_task)
        self.completed_button.clicked.connect(self.mark_as_done)

    def add_task(self):
        """
        Create the Add Task window and append it to the list of windows.
        """
        form = AddTask(self.datacomm)
        self.windows.append(form)

    def remove_task(self):
        """
        Calls a data communication function to remove a task.
        """
        self.datacomm.delete_task()

    def edit_task(self):
        self.myWidget = MyWidget()
        self.myWidget.show()
        self.edit_task_button.setEnabled(False)
        self.edit_task_button.setDisabled(True)
		
    def mark_as_done(self):
        """
        Marks a selected task as Completed.
        """
        # get the indices of the selected rows
        indices = self.task_table.selectionModel().selectedRows()
        for i in indices:
            # get list of tuples containing the selected data
            data = self.table_model.table_data[i.row()]
            # find and update the task with the same data
            for task in self.datacomm.data:
                if all(i == j for i, j in zip(task.values(), data)):
                    task["Completed"] = True
        self.update_table()

    def update_table(self):
        """
        Gets the new data from the data communication and updates the TableView
        """
        self.table_model.table_data = self.datacomm.update()
        self.task_table.setSortingEnabled(True)
        self.task_table.setModel(self.table_model)
        self.task_table.resizeRowsToContents()

    def closeEvent(self, event):
        """
        Reimplementing the closeEvent handler to close all windows when the main
        window is closed.
        """
        qApp.quit()
