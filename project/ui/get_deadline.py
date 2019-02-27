from random import shuffle

from PySide2.QtWidgets import QWidget
from .ui_files.ui_add_deadline import Ui_deadline_form


class AddDeadline(QWidget, Ui_deadline_form):
    """
    Class containing the window for getting the Deadline of a Task.

    Attributes:
        width (int): Width of the window
        height (int): Height of the window
        comboboxes (list of str): Names of the comboboxes in the window.
    """

    def __init__(self, task):
        super().__init__()
        self.width, self.height = 1000, 400

        self.init_UI()
        self.comboboxes = [i for i in vars(self) if i.startswith("comboBox")]
        self.setup_combobox()

    def init_UI(self):
        """
        Load the .ui-converted .py file, set the size and display the window.
        """
        self.setupUi(self)
        self.setFixedSize(self.width, self.height)
        self.show()

    def setup_combobox(self):
        """
        Adds a random ordering of numbers to each combobox in the window.
        """
        options = [
            "4-5+1", "0!", "23%3", "7//2", "58%6", "31.5/6.3", "50//8", "15-8", "2^3", "√81", "100//10"
        ]
        for txt in self.comboboxes:
            shuffle(options)
            for option in options:
                combobox = getattr(self, txt)
                combobox.addItem(option)
