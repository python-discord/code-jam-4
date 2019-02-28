import sys
from random import randint

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QColor, QCursor, QIcon, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog,
                             QMainWindow, QPushButton)

# QBrush

"""
Hover on QPaint detection
def paintEvent(self, event):
    option = QtGui.QStyleOptionButton()
    option.initFrom(self)
    painter = QtGui.QPainter(self)
    if option.state & QtGui.QStyle.State_MouseOver:
        # do hover stuff ...
    else:
        # do normal stuff ...
"""


class ColorBox(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.toolsX = 5
        self.toolsY = 0
        self.tools_holder = 1
        self.exists = True
        self.Setup()

    def Setup(self):
        # self.setGeometry(990, 150, 150, 300)
        self.setWindowTitle('Colorbox')
        self.setFixedSize(150, 300)

    def addPallette(self, pallet):
        pallet.setGeometry(self.toolsX, self.toolsY, 40, 40)
        self.layout().addWidget(pallet)
        self.toolsX += 50
        self.tools_holder += 1
        if self.tools_holder == 4:
            self.toolsX = 5
            self.toolsY += 50
            self.tools_holder = 1

    def showColorBox(self):
        print('Showing ToolBox')
        self.show()

    def closeEvent(self, *args, **kwargs):
        self.exists = False
        print("Closing color pallet window")


class PalletteButton:
    def __init__(self):
        self.r = randint(0, 255)
        self.g = randint(0, 255)
        self.b = randint(0, 255)
        self.t = 1.0  # no transparancy now, it goes from 0.0 to 1.0
        self.color = (self.r, self.g, self.b, self.t)
        # self.color = QColor(self.r, self.g, self.b, self.t)

    def mixColor(self, tool):
        if tool.toolName in ["fill_empty", "straggly_paintbrush",
                             "solidified_brush"]:
            # tool[r,b,g]  ERROR PRONE IF QCOLOR NOT WORK AS TUPLE
            if not ((tool[0] and tool[1] and tool[2]) and self.t):
                tool.color = self.color
            else:  # perhaps don't divide by 4
                mixedColor = QColor(
                    self.r - (max(self.r, tool.color[0] // 4) -
                              min(self.r, tool.color[0] // 4)),
                    self.g - (max(self.g, tool.color[1] // 4) -
                              min(self.g, tool.color[1] // 4)),
                    self.b - (max(self.b, tool.color[2] // 4) -
                              min(self.b, tool.color[2] // 4)),
                    255
                )
                self.color, tool.color = mixedColor, mixedColor
                if tool.toolName in ["straggly_paintbrush",
                                     "solidified_brush"]:
                    tool.isDipped = True


class Tool():
    def __init__(self, toolName, brushSize, color,
                 paintPattern, PaintBoard, iconPath, shortcut, statusTip,
                 isDipped=False
                 ):
        """class for creating drawing tools

        Arguments:
            toolName {str} -- Tools name for display
            duration {float} -- duration
            brushSize {float} -- tools brushsize
            color {QColor} -- the Color to be used
            paintPattern {PaintPattern} -- the paint pattern that will be used
            PaintBoard {PaintBoard} -- Its a paintboard?
            iconPath {str} -- the path to the icon. duh...
            shortcut {str} -- well. its a shortcut. nothing less, nothing more.
            statusTip {str} -- the status tip that will be displayed...
        """

        self.toolName = toolName
        # self.duration = duration
        self.brushSize = brushSize
        self.color = color
        self.isDipped = isDipped
        self.paintPattern = paintPattern
        self.PaintBoard = PaintBoard
        self.iconPath = iconPath
        self.shortcut = shortcut
        self.statusTip = statusTip

        self.create_button()

    def create_button(self):
        tool_btn = QAction(
            QIcon(self.iconPath),
            self.toolName,
            parent=self.PaintBoard
        )

        tool_btn.setShortcut(self.shortcut)
        tool_btn.setStatusTip(self.statusTip)
        tool_btn.triggered.connect(
            lambda: self.PaintBoard.changePaintBoardVars(
                self.toolName,
                self.brushSize,
                self.color,
                self.paintPattern
            )
        )
        self.PaintBoard.toolbar.addAction(tool_btn)


class PaintBoard(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(1000, 500)
        self.setWindowTitle('ArtiQule')
        self.setWindowIcon(QIcon("Design/icons/app_logo.png"))
        self.Setup()

    def Setup(self):
        self.canvas = QImage(self.size(), QImage.Format_RGB32)
        self.canvas.fill(Qt.white)
        self.changePaintBoardVars()
        self.painter = QPainter(self.canvas)
        self.ToolDead = False

        # patterns = []   # TODO: custom paintPatterns here

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

        colorMenu = mainMenu.addMenu("Colors")

        toggleColors = QAction("Show Color Pallette", self)
        colorMenu.addAction(toggleColors)

        colorMenu.triggered.connect(self.colorBoxRun)
        new_canvas_action.triggered.connect(self.newCanvas)
        open_file_action.triggered.connect(self.openFile)
        save_file_action.triggered.connect(self.saveFile)
        exit_action.triggered.connect(self.exit)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setStyleSheet('background-color: white')

        self.pointy_pen = Tool("Pointy Pen", 1, Qt.black,
                               [randint(1, 4), randint(1, 2), randint(0, 3),
                                randint(0, 5)], self,
                               "Design/icons/Pointy Pen.png",
                               "CTRL+P", "A very pointy pen"
                               )

        self.fill = Tool("A Bucket", 2000, Qt.black,
                         [1, 1, 1, 1], self,
                         'Design/icons/A bucket.png',
                         "CTRL+B", "A bucket"
                         )

        self.straggly_paintbrush = Tool("Straggly Paintbrush",
                                        10, Qt.black,
                                        [randint(1, 4), randint(1, 2),
                                         randint(0, 3), randint(0, 5)],
                                        self,
                                        "Design/icons/Straggly Paintbrush.png",
                                        "CTRL+A", "A very Straggly Paintbrush."
                                        )

        self.solidifed_brush = Tool("Solid Brush", 10, Qt.black,
                                    [randint(1, 4), randint(1, 2),
                                     randint(0, 3), randint(0, 5)], self,
                                    'Design/icons/Solid Brush.png',
                                    "CTRL+J", "Gosh, that is a hard tip"
                                    )

        self.eraser = Tool("Eraser", 10, Qt.white,
                           [0, 0, 0, 0], self, "", "Ctrl+F",
                           "Erase Your Mistakes, Kid!")

        self.show()

        self.drawing = False
        self.lastPoint = QPoint()

    def changePaintBoardVars(self, curToolName=None,
                             curBrushsize=1, curBrushColor=None,
                             curPaintPattern=Qt.SolidLine):

        self.currentToolName = curToolName
        self.currentBrushSize = curBrushsize
        self.currentPaintPattern = curPaintPattern
        self.currentBrushColor = curBrushColor
        self.currentToolDuration = randint(5, 10)
        print(self.currentToolName)
        print(self.currentToolDuration)
        print(self.currentBrushSize)

        self.setCursor(QCursor(
            QPixmap("Design/icons/{}.png".format(self.currentToolName
                                                 if self.currentToolName
                                                 else None
                                                 ))))

    # TODO: make a variable self.currentTool
    #  that'll hold the current selected tool, i fixed the class
    # TODO: check if window already exists if not make one
    def colorBoxRun(self):

        colorBox = ColorBox(self)

        geo = self.geometry()
        geo.moveLeft(geo.right())  # moves window right
        colorBox.setGeometry(geo)

        p1, p2, p3, p4, p5, p6 = (QPushButton() for _ in range(6))

        c1 = PalletteButton()
        c2 = PalletteButton()
        c3 = PalletteButton()
        c4 = PalletteButton()
        c5 = PalletteButton()
        c6 = PalletteButton()

        p1.setStyleSheet("background-color: rgba{0}"
                         .format(c1.color))
        p1.clicked.connect(lambda: c1.mixColor(self.currentTool))
        colorBox.addPallette(p1)
        p2.setStyleSheet("background-color: rgba{0}"
                         .format(c2.color))
        p2.clicked.connect(lambda: c2.mixColor(self.currentTool))
        colorBox.addPallette(p2)
        p3.setStyleSheet("background-color: rgba{0}"
                         .format(c3.color))
        p3.clicked.connect(lambda: c3.mixColor(self.currentTool))
        colorBox.addPallette(p3)
        p4.setStyleSheet("background-color: rgba{0};"
                         .format(c4.color))
        p4.clicked.connect(lambda: c4.mixColor(self.currentTool))
        colorBox.addPallette(p4)
        p5.setStyleSheet("background-color: rgba{0}"
                         .format(c5.color))
        p5.clicked.connect(lambda: c5.mixColor(self.currentTool))
        colorBox.addPallette(p5)
        p6.setStyleSheet("background-color: rgba{0}"
                         .format(c6.color))
        p6.clicked.connect(lambda: c6.mixColor(self.currentTool))
        colorBox.addPallette(p6)

        # showing toolBox
        colorBox.showColorBox()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            if self.currentToolName == "A Bucket":
                Pen = QPen()
                Pen.setWidth(self.currentBrushSize)
                Pen.setColor(self.currentBrushColor)
                self.painter.setPen(Pen)
                self.painter.drawLine(0, 0, 1000, 500)
            self.lastPoint = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and\
                self.drawing and self.currentToolName is not None:

            Pen = QPen()
            if self.currentToolName != "A Bucket" and \
                    self.currentToolName != "Eraser":
                if self.currentToolDuration <= 0.0:
                    self.ToolDead = True
                    print('Tools Died')
                    self.currentToolDuration = 0
                    Pen.setDashPattern([0, 0, 0, 0])
                    self.drawing = False
                else:
                    self.ToolDead = False
                    self.currentToolDuration -= 0.01
                # print(self.currentToolDuration)

            if self.currentToolDuration < 1.5:
                size_of_dashes = self.currentPaintPattern
                Pen.setDashPattern(size_of_dashes)

            if self.currentToolName == "Pointy Pen":
                Pen.setCapStyle(Qt.RoundCap)
                Pen.setJoinStyle(Qt.BevelJoin)
            elif self.currentToolName == "Straggly Paintbrush" or \
                    "Solid Brush":
                Pen.setCapStyle(Qt.SquareCap)
                Pen.setJoinStyle(Qt.MiterJoin)
            Pen.setColor(self.currentBrushColor)
            Pen.setWidth(self.currentBrushSize)
            self.painter.setPen(Pen)
            if self.ToolDead is True:
                if self.currentToolName == "Pointy Pen":
                    self.setCursor(QCursor(
                        QPixmap("Design/icons/Pointy Pen Broken.png")))
            # if event.pos().y() > 53 and self.currentToolName is not None:
            self.painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseRealeaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(),
                                 self.canvas, self.canvas.rect())

    def newCanvas(self):
        # TODO: Add New Canvas
        Pen = QPen()
        Pen.setWidth(5000)
        Pen.setColor(Qt.white)
        self.painter.setPen(Pen)
        self.painter.drawLine(0, 0, 1000, 500)
        self.update()
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
