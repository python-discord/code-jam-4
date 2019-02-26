from random import randint, shuffle

from PySide2.QtWidgets import QWidget
from .ui_files.ui_add_deadline import Ui_deadline_form


class AddDeadline(QWidget, Ui_deadline_form):
    def __init__(self, task):
        super().__init__()
        self.width, self.height = 600, 500

        self.init_UI()
        self.comboboxes = [i for i in vars(self) if i.startswith("comboBox")]
        self.setup_combobox()

    def init_UI(self):
        self.setupUi(self)
        self.setFixedSize(self.width, self.height)
        self.show()

    def setup_combobox(self):
        options = [
            "0", "1", "10", "11", "100", "101", "110", "111", "1000", "1001", "1010"
        ]
        for txt in self.comboboxes:
            shuffle(options)
            for option in options:
                combobox = getattr(self, txt)
                combobox.addItem(option)
