import sys
from random import randint
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QAction, QFileDialog, QPushButton)
from PyQt5.QtGui import QImage, QPainter, QPen, QPixmap, QIcon, QCursor

"""Hover on QPaint detection
def paintEvent(self, event):
    option = QtGui.QStyleOptionButton()
    option.initFrom(self)
    painter = QtGui.QPainter(self)
    if option.state & QtGui.QStyle.State_MouseOver:
        # do hover stuff ...
    else:
        # do normal stuff ...
"""


class ToolBox(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.toolsX = 5
        self.toolsY = 0
        self.tools_holder = 1
        self.Setup()

    def Setup(self):
        # self.setGeometry(990, 150, 150, 300)
        self.setWindowTitle('ToolBox')
        self.setFixedSize(150, 300)

    def addTools(self, pallet):
        pallet.setGeometry(self.toolsX, self.toolsY, 40, 40)
        self.layout().addWidget(pallet)
        self.toolsX += 50
        self.tools_holder += 1
        if self.tools_holder == 4:
            self.toolsX = 5
            self.toolsY += 50
            self.tools_holder = 1

    def ShowToolBox(self):
        print('Showing ToolBox')
        self.show()


class PaintBoard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(1000, 800)
        self.setWindowTitle('ArtiQule')
        self.setWindowIcon(QIcon("Design/icons/app_logo.png"))

        self.stylesheet = ""

        self.Setup()

    # Setting up the window form
    def Setup(self):

        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.white)

        self.draw = False
        self.brushSize = 1
        self.Color = Qt.black
        self.paintPattern = Qt.SolidLine

        self.lastPoint = QPoint()

        # patterns = []   # TODO: custom paintPatterns here

        # class PaletteButton:
        #     def __init__(self):
        #         self.color = Qt.Color(randint(0, 255),
        #                               randint(0, 255),
        #                               randint(0, 255))

        # def mix(self, tool):
        #     print('mix')

        class Tool:
            def __init__(self, toolName, brushSize,
                         paintPattern=Qt.SolidLine, duration=randint(0, 10)):
                self.toolName = toolName
                self.brushSize = brushSize
                self.paintPattern = paintPattern
                self.duration = duration

            def set_icon(self):
                PaintBoard.setCursor(QCursor(QIcon(
                    QPixmap("Design/icons/{}.png".format(self.toolName)))))

            def use(self):
                self.set_icon()
                PaintBoard.paintPattern = self.paintPattern

        class PointyPen(Tool):
            def __init__(self):
                super().__init__("pointy_pen", 5)

        class ColorTool(Tool):
            def __init__(self, toolName, brushSize, paintPattern=None,
                         duration=randint(0, 30), color=None):
                super().__init__(toolName, brushSize, paintPattern, duration)
                self.color = color

            def use(self):
                self.set_icon()
                PaintBoard.paintPattern = self.paintPattern
                PaintBoard.brushColor = self.color

        # paintpattern like straggly straws
        class StragglyPaintBrush(ColorTool):
            def __init__(self):
                super().__init__("straggly_paintbrush", 30, "Straws")

        # like drawing with a rock hard paintbrush
        class SolidifiedBrush(ColorTool):
            def __init__(self):
                super().__init__("solidified_brush", 50, False, 1)

        class Fill(ColorTool):
            def __init__(self):
                # a big color dump
                super().__init__("fill_empty", 500, "big dump", 1)

        fill = Fill()
        pointy_pen = PointyPen()
        solidified_brush = SolidifiedBrush()
        straggly_paintbrush = StragglyPaintBrush()

        # Setting the size to be fixed

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('File')
        toolsMenu = mainMenu.addMenu('Tools')

        color_pallet_action = QAction('ToolBox', self)
        color_pallet_action.setShortcut('Ctrl+H')

        new_canvas_action = QAction('New File', self)
        new_canvas_action.setShortcut('Ctrl+N')

        open_file_action = QAction('Open File', self)
        open_file_action.setShortcut('Ctrl+O')

        save_file_action = QAction('Save File', self)
        save_file_action.setShortcut('Ctrl+S')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Alt+F4')

        toolsMenu.addAction(color_pallet_action)
        fileMenu.addAction(new_canvas_action)
        fileMenu.addAction(open_file_action)
        fileMenu.addAction(save_file_action)
        fileMenu.addAction(exit_action)

        color_pallet_action.triggered.connect(self.toolBox)
        new_canvas_action.triggered.connect(self.newCanvas)
        open_file_action.triggered.connect(self.openFile)
        save_file_action.triggered.connect(self.saveFile)
        exit_action.triggered.connect(self.exit)

        # toolbar picker
        # self.toolBox = QToolBox(self)
        # self.toolBox.setSizePolicy(QSizePolicy(
        #     QSizePolicy.Maximum, QSizePolicy.Ignored))
        # self.toolBox.setGeometry(0, 20, 80, 150)

        # self.toolBox.setMinimumWidth(self.sizeHint().width())
        pointy_pen_btn = QPushButton()
        pointy_pen_btn.setShortcut("CTRL+P")
        pointy_pen_btn.setStatusTip("A very pointy pen")
        # pointy_pen.setGeometry(200, 0, 50, 20)
        pointy_pen_btn.clicked.connect(pointy_pen.use)
        pointy_pen_btn.setIcon(QIcon('Design/icons/pointy_pen.png'))
        pointy_pen_btn.setIconSize(QSize(20, 20))
        # self.toolBox.addItem(pointy_pen_btn, "Pointy Pen")

        fill_btn = QPushButton()
        fill_btn.setShortcut("CTRL+P")
        fill_btn.setStatusTip("A bucket.")
        # fill.setGeometry(200, 0, 50, 20)
        fill_btn.clicked.connect(fill.use)
        fill_btn.setIcon(QIcon('Design/icons/fill_empty.png'))
        fill_btn.setIconSize(QSize(20, 20))
        # self.toolBox.addItem(fill_btn, "Bucket")

        straggly_paintbrush_btn = QPushButton()
        straggly_paintbrush_btn.setShortcut("CTRL+A")
        straggly_paintbrush_btn.setStatusTip("A very Straggly Paintbrush.")
        # fill.setGeometry(200, 0, 50, 20)
        straggly_paintbrush_btn.clicked.connect(straggly_paintbrush.use)
        straggly_paintbrush_btn.setIcon(
            QIcon('Design/icons/straggly_paintbrush.png'))
        straggly_paintbrush_btn.setIconSize(QSize(20, 20))
        # self.toolBox.addItem(straggly_paintbrush_btn, "Straggly Paintbrush")

        solidified_brush_btn = QPushButton()
        solidified_brush_btn.setShortcut("CTRL+A")
        solidified_brush_btn.setStatusTip("Gorsh, that is a hard tip")
        # fill.setGeometry(200, 0, 50, 20)
        solidified_brush_btn.clicked.connect(solidified_brush.use)
        solidified_brush_btn.setIcon(
            QIcon('Design/icons/solidified_brush.png'))
        solidified_brush_btn.setIconSize(QSize(20, 20))
        # self.toolBox.addItem(solidified_brush_btn, "Solidified Brush")

        self.show()

    # if RGB is 0 (white) then recieve only that color;
    # else mix by taking current color RGB and adding/subtracting on palette
    # solidified_brush and spangly_brush will drip
    # if they are put in color palette
    def color_palette(self):
        # TODO: add color pallet window
        print('color pallet')

    def toolBox(self):
        toolBox = ToolBox(self)
        geo = self.geometry()
        geo.moveLeft(geo.left())
        toolBox.setGeometry(geo)
        # Testing purposes
        fake_green = QPushButton('Green')
        fake_green.setStyleSheet('background-color: green')
        fake_red = QPushButton('Red')
        fake_red.setStyleSheet('background-color: red')
        fake_blue = QPushButton('Blue')
        fake_blue.setStyleSheet('background-color: blue')
        fake_yellow = QPushButton('Yellow')
        fake_yellow.setStyleSheet('background-color: yellow')
        toolBox.addTools(fake_red)
        toolBox.addTools(fake_green)
        toolBox.addTools(fake_blue)
        toolBox.addTools(fake_yellow)
        # showing toolBox
        toolBox.ShowToolBox()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.draw:
            painter = QPainter(self.canvas)
            # might modify roundcap is necessary
            painter.setPen(QPen(self.Color, self.brushSize,
                                self.paintPattern, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseRealeaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw = False

    def paintEvent(self, event):
        # print('paintevent')
        if self.draw:
            canvas_painter = QPainter(self)
            canvas_painter.drawImage(self.rect(),
                                     self.canvas, self.canvas.rect())

    def newCanvas(self):
        # TODO: Add New Canvas
        print('new canvas')

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileNames(
            self,
            "Open File",
            "Load Image",
            "PNG(*.png);; JPG(*.jpg *.jpeg)",
            options=options)

    def saveFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image", "",
            "PNG(*.png);;JPEG(*.jpg *.jpeg)")

        if filePath:
            print(filePath)
            # with open(filePath, "w+") as file:
            # self.canvasPainter.save()
            # file.write(filePath)
            # img = Image.open(filePath)
            # img.save(filePath)

    def exit(self):
        raise SystemExit


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow{background-color:white}")
    myGUI = PaintBoard()

    sys.exit(app.exec_())
