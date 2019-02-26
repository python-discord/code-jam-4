from PyQt5.QtWidgets import QDialog
from ui.eula import Ui_EulaDialog

class EulaDialog(QDialog, Ui_EulaDialog):
    def __init__(self, eula):
        super(EulaDialog, self).__init__()
        self.setupUi(self)
        self.eula_TextEdit.setPlainText(eula)