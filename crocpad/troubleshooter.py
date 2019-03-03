from pathlib import Path

from PyQt5.QtWidgets import QWizard, QMessageBox
from PyQt5.QtMultimedia import QSound

from crocpad.ui.wizard import Ui_Wizard


class Troubleshooter(QWizard, Ui_Wizard):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        song_path = str(Path('crocpad') / Path('good.wav'))
        self.song = QSound(song_path)
        self.song.play()
        self.song.setLoops(99999999)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "LET ME FINISH.",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()

    def reject(self):
        self.close()
