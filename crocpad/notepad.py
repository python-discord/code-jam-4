import random
import sys
from zipfile import BadZipFile

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget,
                             QFileDialog, QMainWindow, QMessageBox,
                             QPlainTextEdit, QStatusBar, QVBoxLayout, QWidget)

from crocpad.configuration import app_config, save_config
from crocpad.eula_dialog import EulaDialog
from crocpad.eula_quiz_dialog import EulaQuizDialog
import crocpad.stylesheets


class MainWindow(QMainWindow):

    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.app = app
        self.main_window = QPlainTextEdit()

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(24)
        self.main_window.setFont(QFont('Comic Sans MS', 30))
        self.main_window.installEventFilter(self)
        self.sound = QSound("crocpad\\sounds\\click.wav")
        self.enter_sound = QSound("crocpad\\sounds\\scream.wav")
        self.backspace_sound = QSound("crocpad\\sounds\\wrong.wav")

        layout = QVBoxLayout()
        layout.addWidget(self.main_window)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Update title and centre window
        self.update_title()
        self.setGeometry(50, 50, 800, 600)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.setWindowIcon(QIcon('crocpad\\crocpad.ico'))
        self.create_menus()
        self.app.setStyleSheet(crocpad.stylesheets.default)
        self.show()

        # Post-startup tasks
        if app_config['License']['eulaaccepted'] != 'yes':
            self.do_eula()
        if app_config['Editor']['tips'] == 'on':
            self.show_tip()

    def create_menus(self):
        mainMenu = self.menuBar()
        helpMenu = mainMenu.addMenu('H&elp')
        viewMenu = mainMenu.addMenu('Vi&ew')
        fileMenu = mainMenu.addMenu('R&ecent Files')
        editMenu = mainMenu.addMenu('&Edit')
        searchMenu = mainMenu.addMenu('S&earch')
        toolsMenu = mainMenu.addMenu('&Tools')

        # Help menu
        action_tip = QAction("Tip of th&e Day", self)
        action_tip.triggered.connect(self.show_tip)
        helpMenu.addAction(action_tip)

        # View menu
        themeMenu = viewMenu.addMenu("Themes")
        action_light_theme = QAction("Light mod&e", self)
        action_light_theme.triggered.connect(self.set_light_theme)
        themeMenu.addAction(action_light_theme)
        action_dark_theme = QAction("Dark mod&e", self)
        action_dark_theme.triggered.connect(self.set_dark_theme)
        themeMenu.addAction(action_dark_theme)
        accessibilityMenu = viewMenu.addMenu("Accessibility")
        action_hotdogstand_theme = QAction("High visibility th&eme", self)
        action_hotdogstand_theme.triggered.connect(self.set_hotdogstand_theme)
        accessibilityMenu.addAction(action_hotdogstand_theme)
        action_quitedark_theme = QAction("Th&eme for blind users", self)
        action_quitedark_theme.triggered.connect(self.set_quitedark_theme)
        accessibilityMenu.addAction(action_quitedark_theme)

        # Search menu
        action_open = QAction("S&earch for file to open", self)
        action_open.triggered.connect(self.open_file)
        searchMenu.addAction(action_open)
        action_save = QAction("S&earch for file to save", self)
        action_save.triggered.connect(self.save_file)
        searchMenu.addAction(action_save)
        action_new = QAction("S&earch for a new f&ile", self)
        action_new.triggered.connect(self.new_file)
        searchMenu.addAction(action_new)

        # SubMenu Test
        testmenu = []
        for i in range(0, 200):
            testmenu.append(fileMenu.addMenu(f'{i}'))

    def do_eula(self):
        with open('crocpad\\EULA.txt', 'r', encoding='utf8') as f:
            eula = f.read()
        self.eula_dialog = EulaDialog(eula)
        self.eula_quiz_dialog = EulaQuizDialog()
        while not self.eula_quiz_dialog.quiz_correct():
            self.eula_dialog.exec_()
            if self.eula_dialog.clicked_button == self.eula_dialog.eula_agree_button:
                # We click the agree button
                app_config['License']['eulaaccepted'] = 'yes'
                save_config(app_config)
            self.eula_quiz_dialog.exec_()

    def show_tip(self):
        with open('crocpad\\tips.txt', 'r', encoding='utf8') as f:
            tips = f.readlines()
        tip = random.choice(tips)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Tip of the Day")
        dlg.setText(tip.strip())
        dlg.setIcon(QMessageBox.Information)
        dlg.show()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if app_config['Sound']['sounds'] == 'on':
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    self.sound.stop()
                    self.enter_sound.play()
                if event.key() == Qt.Key_Backspace:
                    self.sound.stop()
                    self.backspace_sound.play()
                else:
                    self.sound.play()
            if event.key() == Qt.Key_Space:
                if random.random() > 0.8:
                    dlg = QMessageBox(self)
                    dlg.setWindowTitle("Are you sure?")
                    dlg.setText("_" * 100)
                    dlg.show()
                    dlg.close()
        return False

    def dialog_critical(self, alert_text):
        dlg = QMessageBox(self)
        dlg.setText(alert_text)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def update_title(self):
        self.setWindowTitle("Crocpad++")

    def edit_toggle_wrap(self):
        self.main_window.setLineWrapMode(not self.main_window.lineWrapMode())

    def open_file(self):
        filename = QFileDialog.getOpenFileName()[0]
        with open(filename, 'r') as file:
            self.main_window.setPlainText(file.read())

    def save_file(self):
        filename = QFileDialog.getSaveFileName()[0]
        text = self.main_window.document().toPlainText()
        with open(filename, 'w') as file:
            file.write(text)

    def new_file(self):
        self.main_window.document().clear()
        self.main_window.insertPlainText("""To remove this message, please make sure you have entered
        your full credit card details, made payable to:
        Crocpad++ Inc
        PO BOX 477362213321233
        Cheshire Cheese
        Snekland
        Australia
        """)

    def set_light_theme(self):
        self.app.setStyleSheet(crocpad.stylesheets.light)

    def set_dark_theme(self):
        self.app.setStyleSheet(crocpad.stylesheets.dark)

    def set_hotdogstand_theme(self):
        self.app.setStyleSheet(crocpad.stylesheets.hotdogstand)

    def set_quitedark_theme(self):
        self.app.setStyleSheet(crocpad.stylesheets.quitedark)
