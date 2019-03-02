from PyQt5.QtWidgets import QMainWindow


class AddItemScreen(QMainWindow):
    """Screen that allows users to manually add some ext """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Item")
