from PyQt5.QtWidgets import QWizard, QApplication, QMessageBox, QWizardPage
from troubleshooterUI import Ui_MainWindow
import wizard
import sys
import music

class Troubleshooter(QWizard, wizard.Ui_Wizard):
    def __init__(self, pages):
        super(self.__class__, self).__init__()
        self.setupUi(self, pages)
    
    def closeEvent(self, event):
        print("event")
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
        	raise music.StopMusic
        	event.accept()
        else:
            event.ignore()

class WizardPages:

	class page1(QWizardPage, wizard.Ui_WizardPage1):
		def __init__(self):
			super(self.__class__, self).__init__()
			self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    pages = [WizardPages.page1()]
    form = Troubleshooter(pages)
    app.setApplicationName("Crocpad++ Troubleshooter")
    form.show()
    music.play("good.mid")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()