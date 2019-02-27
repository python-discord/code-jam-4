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
        self.width, self.height = 600, 500

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
            "0", "1", "10", "11", "100", "101", "110", "111", "1000", "1001", "1010"
        ]
        for txt in self.comboboxes:
            shuffle(options)
            for option in options:
                combobox = getattr(self, txt)
                combobox.addItem(option)
