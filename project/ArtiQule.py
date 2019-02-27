import sys
from random import randint
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QAction, QFileDialog, QPushButton,
                             QToolBox, QSizePolicy)
from PyQt5.QtGui import (QImage, QPainter, QPen, QPixmap,
                         QIcon, QCursor, QColor)

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


class PaintBoard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(1000, 500)
        self.setWindowTitle('ArtiQule')
        self.setWindowIcon(QIcon("Design/icons/app_logo.png"))

        self.stylesheet = ""

        self.Setup()

    # Setting up the window form
    def Setup(self):

        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.white)

        self.draw = False
        self.currentBrushSize = 1  # TODO: only active when mouseAction allows
        self.currentBrushColor = Qt.black
        self.currentPaintPattern = Qt.SolidLine

        self.lastPoint = QPoint()

        # patterns = []   # TODO: custom paintPatterns here

        class PaletteButton:
            def __init__(self):
                self.r = randint(0, 255)
                self.g = randint(0, 255)
                self.b = randint(0, 255)
                self.t = 255  # No transparancy now
                self.color = QColor(self.r,
                                    self.g,
                                    self.b,
                                    self.t)

            def mix_color(self, tool):
                if isinstance(type(tool), ColorTool):
                    if not ((tool.r and tool.g and tool.r) and self.t):
                        tool.color = self.color
                    else:  # perhaps don't divide by 4
                        mixedColor = QColor(
                            self.r - (max(self.r, tool.r//4) - min(self.r, tool.r//4)),
                            self.g - (max(self.g, tool.g//4) - min(self.g, tool.g//4)),
                            self.b - (max(self.b, tool.b//4) - min(self.b, tool.b//4)),
                            255
                            )
                        self.color, tool.color = mixedColor, mixedColor
                        tool.is_dipped = True


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

            def use(self):
                self.set_icon()
                PaintBoard.paintPattern = self.paintPattern

                while self.duration:
                    PaintBoard.draw = True  # error prone


        class ColorTool(Tool):
            def __init__(self, toolName, brushSize, paintPattern=None,
                         duration=randint(0, 30), r=0, g=0, b=0, t=0):
                super().__init__(toolName, brushSize, paintPattern, duration)
                self.r = r                           # TODO: less duration, more transprancy
                self.g = g
                self.b = b
                self.t = 0
                self.color = QColor(self.r,
                                    self.g,
                                    self.b,
                                    self.t)
                self.is_dipped = False

            def use(self):
                self.set_icon()
                PaintBoard.paintPattern = self.paintPattern
                PaintBoard.brushColor = self.color

                # while tool is used, duration seconds will go down,
                # leading to less transparancy

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

        new_canvas_action = QAction('New File', self)
        new_canvas_action.setShortcut('Ctrl+N')

        open_file_action = QAction('Open File', self)
        open_file_action.setShortcut('Ctrl+O')

        save_file_action = QAction('Save File', self)
        save_file_action.setShortcut('Ctrl+S')

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Alt+F4')

        fileMenu.addAction(new_canvas_action)
        fileMenu.addAction(open_file_action)
        fileMenu.addAction(save_file_action)
        fileMenu.addAction(exit_action)

        new_canvas_action.triggered.connect(self.newCanvas)
        open_file_action.triggered.connect(self.openFile)
        save_file_action.triggered.connect(self.saveFile)
        exit_action.triggered.connect(self.exit)

        # toolbar picker
        self.toolBox = QToolBox(self)
        self.toolBox.setSizePolicy(QSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Ignored))
        self.toolBox.setGeometry(0, 20, 50, 100)

        # self.toolBox.setMinimumWidth(self.sizeHint().width())
        pointy_pen_btn = QPushButton()
        pointy_pen_btn.setShortcut("CTRL+P")
        pointy_pen_btn.setStatusTip("A very pointy pen")
        # pointy_pen.setGeometry(200, 0, 50, 20)
        pointy_pen_btn.clicked.connect(pointy_pen.use)
        pointy_pen_btn.setIcon(QIcon('Design/icons/pointy_pen.png'))
        pointy_pen_btn.setIconSize(QSize(20, 20))
        self.toolBox.addItem(pointy_pen_btn, "Pointy Pen")

        fill_btn = QPushButton()
        fill_btn.setShortcut("CTRL+P")
        fill_btn.setStatusTip("A bucket.")
        # fill.setGeometry(200, 0, 50, 20)
        fill_btn.clicked.connect(fill.use)
        fill_btn.setIcon(QIcon('Design/icons/fill_empty.png'))
        fill_btn.setIconSize(QSize(20, 20))
        self.toolBox.addItem(fill_btn, "Bucket")

        straggly_paintbrush_btn = QPushButton()
        straggly_paintbrush_btn.setShortcut("CTRL+A")
        straggly_paintbrush_btn.setStatusTip("A very Straggly Paintbrush.")
        # fill.setGeometry(200, 0, 50, 20)
        straggly_paintbrush_btn.clicked.connect(straggly_paintbrush.use)
        straggly_paintbrush_btn.setIcon(
            QIcon('Design/icons/straggly_paintbrush.png'))
        straggly_paintbrush_btn.setIconSize(QSize(20, 20))
        self.toolBox.addItem(straggly_paintbrush_btn, "Straggly Paintbrush")

        solidified_brush_btn = QPushButton()
        solidified_brush_btn.setShortcut("CTRL+A")
        solidified_brush_btn.setStatusTip("Gorsh, that is a hard tip")
        # fill.setGeometry(200, 0, 50, 20)
        solidified_brush_btn.clicked.connect(solidified_brush.use)
        solidified_brush_btn.setIcon(
            QIcon('Design/icons/solidified_brush.png'))
        solidified_brush_btn.setIconSize(QSize(20, 20))
        self.toolBox.addItem(solidified_brush_btn, "Solidified Brush")

        color_palette_btn = QPushButton()
        # p1
        # p2
        # p3
        # p4
        # p5
        # p6

        self.toolBox.addItem(color_palette_btn, "Colors")

        self.show()

    # if RGB is 0 (white) then recieve only that color;
    # else mix by taking current color RGB and adding/subtracting on palette
    # solidified_brush and spangly_brush will drip
    # if they are put in color palette
    def color_palette(self, tool):
        pass

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.draw:
            painter = QPainter(self.canvas)
            # might modify roundcap is necessary
            painter.setPen(QPen(self.brushColor, self.brushSize,
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
        self.canvasPainter.resetTransform()
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
