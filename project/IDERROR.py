import sys
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.Qsci import QsciLexerPython, QsciScintilla

# specifying the location of the Design
form_ui = 'Design/Editor.ui'
Ui_MainWindow, QtBaseClass = loadUiType(form_ui)


class Editor(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.setupUi(self)

    # Setting up the window form
    def Setup(self):
        # Setting the size to be fixed
        self.setFixedSize(800, 800)
        self.setWindowTitle('[E.E] IDERROR')

        # MenuBar
        bar = self.menubar

        File = bar.addMenu('File')

        new_file_action = QAction('New File', self)
        new_file_action.setShortcut('Ctrl+N')

        open_file_action = QAction('Open File', self)
        open_file_action.setShortcut('Ctrl+O')

        save_file_action = QAction('Save File', self)
        save_file_action.setShortcut('Ctrl+S')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Alt+F4')

        File.addAction(new_file_action)
        File.addAction(open_file_action)
        File.addAction(save_file_action)
        File.addAction(exit_action)

        new_file_action.triggered.connect(self.newFile)
        open_file_action.triggered.connect(self.openFile)
        save_file_action.triggered.connect(self.saveFile)
        exit_action.triggered.connect(self.exit)

        # Custom Editor Widget:

        # adding the the custom editor of QsciScintilla
        self.editor = QsciScintilla()
        self.editor.setGeometry(25, 25, 750, 750)
        # adding text to the ditro
        self.editor.append("print('Hello World!') # this is just a test")
        # syntax adding and autocomplete configuration
        self.python_syntax = QsciLexerPython()
        self.editor.setLexer(self.python_syntax)
        self.editor.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.editor.setAutoCompletionCaseSensitivity(True)
        self.editor.setAutoCompletionThreshold(2)
        self.editor.setAutoCompletionReplaceWord(False)
        self.editor.setIndentationsUseTabs(True)
        self.editor.setTabWidth(4)
        self.editor.setIndentationGuides(True)
        self.editor.setTabIndents(True)
        self.editor.setAutoIndent(False)
        self.editor.setUtf8(True)  # Set encoding to UTF-8
        # setting editor position

        # adding font
        self.Font = QFont()
        # adding text size
        self.Font.setPointSize(16)
        # applying font
        self.editor.setFont(self.Font)  # Will be overridden by lexer!
        # adding the editor to te form
        self.layout().addWidget(self.editor)

        # showing ui
        self.show()

    def newFile(self):
        # TODO: Add New Files
        self.editor.setText('')
        print('new file')

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                  "Python Files (*.py)",
                                                  options=options)
        if fileName:
            self.editor.setText('')
            with open(fileName) as file:
                texts = file.readlines()
                for text in texts:
                    self.editor.append(text)

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "",
                                                  "Text Files (*.py)",
                                                  options=options)
        if fileName:
            with open(fileName + '.py', mode="w+") as file:
                texts = self.editor.text()
                print(texts)
                # TODO: there is kinda of bug here where it adds extra
                #  spaces or line returns, do fix it pls
                file.write(texts)
                file.close()

    def exit(self):
        raise SystemExit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myGUI = Editor()
    myGUI.Setup()

    sys.exit(app.exec_())
