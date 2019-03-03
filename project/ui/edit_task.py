import sys
import random
from PySide2 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
	global count
	count = 0
	print("count:", count)
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		
		# self.hello = ["Hallo Welt", "你好，世界", "Hei maailma", "Hola Mundo", "Привет мир"]
		
		self.greetings = ["Are you sure you wanna edit?", "It is weird that you want to edit.", "Why do you want to edit", "I do not think that is a wise choice", "Beep! Beep! Wrong choice!"]
		
		self.button = QtWidgets.QPushButton("Click to edit")
		self.text = QtWidgets.QLabel("Edit Task?")
		self.text.setAlignment(QtCore.Qt.AlignCenter)

		self.layout = QtWidgets.QVBoxLayout()
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.button)
		self.setLayout(self.layout)
	
		self.button.clicked.connect(self.magic)
		
	def magic(self):
		global count
		print("count:", count)
		if count < 5:
			self.text.setText(random.choice(self.greetings))
			count += 1
		else:
			self.text = QtWidgets.QLabel("Sorry! Wrong Answer! Function is disabled..")
			self.button.setEnabled(False)
			self.button.setDisabled(True)
			return True
		print("count:", count)
		
			

# if __name__ == "__main__":
	# app = QtWidgets.QApplication(sys.argv)
	
	# widget = MyWidget()
	# widget.show()
	
	# sys.exit(app.exec_())