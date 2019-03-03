from PyQt5.QtWidgets import QWizard, QApplication, QMessageBox, QWizardPage
from PyQt5.QtMultimedia import QSound
from PyQt5 import QtCore
import wizard
import sys

class Troubleshooter(QWizard, wizard.Ui_Wizard):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "bro plz", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
        	event.accept()
        else:
            event.ignore()
    def reject(self):
        self.close()

def main():
    app = QApplication(sys.argv)
    form = Troubleshooter()
    app.setApplicationName("crocpad++ troubleshooter")
    form.show()
    song = QSound("good.wav")
    song.play()
    song.setLoops(99999999)
    sys.exit(app.exec_())
    song.stop()

if __name__ == '__main__':
    main()