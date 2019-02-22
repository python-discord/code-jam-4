from PyQt5 import QtWidgets
import sys


class Window(QtWidgets.QMainWindow):
    '''This is a QMainWindow object
    as you can imagine this is the main window :O
    an application doesnt need a mainwindow and you *could* just use a QWidget'''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_gui()

    def setup_gui(self):
        # Create a widget, this is the main widget
        self.main_widget = QtWidgets.QWidget()

        # The widget needs a layout so the stuff inside it looks nice
        main_layout = QtWidgets.QHBoxLayout()
        self.main_widget.setLayout(main_layout)

        # This is how you create a button and link it to a function
        example_button = QtWidgets.QPushButton(self.main_widget)
        example_button.setText("Click me")
        example_button.setStyleSheet("background: blue; color: white;")
        example_button.clicked.connect(self.button_clicked)

        # This is how you add a widget to a layout
        main_layout.addWidget(example_button)
        self.setCentralWidget(self.main_widget)

    def button_clicked(self):
        print("Button clicked!")


if __name__ == '__main__':
    # create the PyQt5 app
    app = QtWidgets.QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())