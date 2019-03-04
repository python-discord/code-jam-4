# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt/mainwindow.ui',
# licensing of 'qt/mainwindow.ui' applies.
#
# Created: Sun Mar  3 15:46:35 2019
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
        self.gridLayout_2 = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 20)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 2, 2, 1, 1)
        self.media_time_lcd = QtWidgets.QLCDNumber(self.central_widget)
        self.media_time_lcd.setDigitCount(8)
        self.media_time_lcd.setMode(QtWidgets.QLCDNumber.Hex)
        self.media_time_lcd.setObjectName("media_time_lcd")
        self.gridLayout_2.addWidget(self.media_time_lcd, 2, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 2, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 3, 1, 1, 1)
        self.playlist_view = QtWidgets.QTableView(self.central_widget)
        self.playlist_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.playlist_view.setStyleSheet(":focus {\n"
"    border: none;\n"
"    outline: none;\n"
"}")
        self.playlist_view.setFrameShape(QtWidgets.QFrame.Box)
        self.playlist_view.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.playlist_view.setAlternatingRowColors(True)
        self.playlist_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.playlist_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.playlist_view.setSortingEnabled(True)
        self.playlist_view.setWordWrap(False)
        self.playlist_view.setObjectName("playlist_view")
        self.playlist_view.horizontalHeader().setHighlightSections(False)
        self.playlist_view.horizontalHeader().setStretchLastSection(False)
        self.gridLayout_2.addWidget(self.playlist_view, 0, 0, 1, 5)
        self.seek_slider = QtWidgets.QSlider(self.central_widget)
        self.seek_slider.setOrientation(QtCore.Qt.Horizontal)
        self.seek_slider.setObjectName("seek_slider")
        self.gridLayout_2.addWidget(self.seek_slider, 2, 1, 1, 1)
        self.media_controls_layout = QtWidgets.QHBoxLayout()
        self.media_controls_layout.setSpacing(10)
        self.media_controls_layout.setObjectName("media_controls_layout")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.media_controls_layout.addItem(spacerItem5)
        self.previous_button = QtWidgets.QPushButton(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_button.sizePolicy().hasHeightForWidth())
        self.previous_button.setSizePolicy(sizePolicy)
        self.previous_button.setObjectName("previous_button")
        self.media_controls_layout.addWidget(self.previous_button)
        self.play_button = QtWidgets.QPushButton(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.play_button.sizePolicy().hasHeightForWidth())
        self.play_button.setSizePolicy(sizePolicy)
        self.play_button.setObjectName("play_button")
        self.media_controls_layout.addWidget(self.play_button)
        self.next_button = QtWidgets.QPushButton(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_button.sizePolicy().hasHeightForWidth())
        self.next_button.setSizePolicy(sizePolicy)
        self.next_button.setObjectName("next_button")
        self.media_controls_layout.addWidget(self.next_button)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.media_controls_layout.addItem(spacerItem6)
        self.volume_slider = QtWidgets.QSlider(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.volume_slider.sizePolicy().hasHeightForWidth())
        self.volume_slider.setSizePolicy(sizePolicy)
        self.volume_slider.setMinimumSize(QtCore.QSize(125, 0))
        self.volume_slider.setBaseSize(QtCore.QSize(0, 0))
        self.volume_slider.setMaximum(100)
        self.volume_slider.setProperty("value", 75)
        self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
        self.volume_slider.setObjectName("volume_slider")
        self.media_controls_layout.addWidget(self.volume_slider)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.media_controls_layout.addItem(spacerItem7)
        self.gridLayout_2.addLayout(self.media_controls_layout, 4, 0, 1, 5)
        MainWindow.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 1064, 20))
        self.menu_bar.setObjectName("menu_bar")
        self.menu_file = QtWidgets.QMenu(self.menu_bar)
        self.menu_file.setObjectName("menu_file")
        MainWindow.setMenuBar(self.menu_bar)
        self.add_files_action = QtWidgets.QAction(MainWindow)
        self.add_files_action.setObjectName("add_files_action")
        self.menu_file.addAction(self.add_files_action)
        self.menu_bar.addAction(self.menu_file.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.media_time_lcd.setToolTip(QtWidgets.QApplication.translate("MainWindow", "<html><head/><body><p>Time remaining for the current track, in hexadecimal seconds.</p></body></html>", None, -1))
        self.previous_button.setText(QtWidgets.QApplication.translate("MainWindow", "Previous", None, -1))
        self.play_button.setText(QtWidgets.QApplication.translate("MainWindow", "Play", None, -1))
        self.next_button.setText(QtWidgets.QApplication.translate("MainWindow", "Next", None, -1))
        self.menu_file.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.add_files_action.setText(QtWidgets.QApplication.translate("MainWindow", "Add files", None, -1))

