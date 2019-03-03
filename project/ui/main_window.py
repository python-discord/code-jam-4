# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/mainwindow.ui',
# licensing of 'qt/mainwindow.ui' applies.
#
# Created: Sun Mar  3 05:37:58 2019
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1064, 563)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.playlist_view = QtWidgets.QTableView(self.central_widget)
        self.playlist_view.setGeometry(QtCore.QRect(20, 20, 1021, 371))
        self.playlist_view.setObjectName("playlist_view")
        self.seek_slider = QtWidgets.QSlider(self.central_widget)
        self.seek_slider.setGeometry(QtCore.QRect(30, 410, 811, 22))
        self.seek_slider.setOrientation(QtCore.Qt.Horizontal)
        self.seek_slider.setObjectName("seek_slider")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.central_widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(420, 450, 254, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.media_controls_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.media_controls_layout.setContentsMargins(0, 0, 0, 0)
        self.media_controls_layout.setObjectName("media_controls_layout")
        self.previous_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.previous_button.setObjectName("previous_button")
        self.media_controls_layout.addWidget(self.previous_button)
        self.play_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.play_button.setObjectName("play_button")
        self.media_controls_layout.addWidget(self.play_button)
        self.next_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.next_button.setObjectName("next_button")
        self.media_controls_layout.addWidget(self.next_button)
        self.media_time_lcd = QtWidgets.QLCDNumber(self.central_widget)
        self.media_time_lcd.setGeometry(QtCore.QRect(870, 410, 171, 23))
        self.media_time_lcd.setDigitCount(8)
        self.media_time_lcd.setMode(QtWidgets.QLCDNumber.Hex)
        self.media_time_lcd.setObjectName("media_time_lcd")
        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1064, 20))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menu_bar)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.add_files_action = QtWidgets.QAction(MainWindow)
        self.add_files_action.setObjectName("add_files_action")
        self.menu_file.addAction(self.add_files_action)
        self.menu_bar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.previous_button.setText(QtWidgets.QApplication.translate("MainWindow", "Previous", None, -1))
        self.play_button.setText(QtWidgets.QApplication.translate("MainWindow", "Play", None, -1))
        self.next_button.setText(QtWidgets.QApplication.translate("MainWindow", "Next", None, -1))
        self.media_time_lcd.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Time remaining for the current track, in hexadecimal seconds.</p></body></html>", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.add_files_action.setText(QtWidgets.QApplication.translate("MainWindow", "Add files", None, -1))

