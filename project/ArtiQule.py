import sys
from random import randint

from PyQt5.QtCore import QPoint, Qt  # , QSize
#  QPushButton, QToolBox, QSizePolicy, QToolButton
from PyQt5.QtGui import QColor, QCursor, QIcon, QImage, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QAction, QApplication, QFileDialog, QMainWindow

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


class Tool():
    def __init__(self, toolName, duration, brushSize, color,
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
        self.duration = duration
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
                self.paintPattern,
                self.duration
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

        new_canvas_action.triggered.connect(self.newCanvas)
        open_file_action.triggered.connect(self.openFile)
        save_file_action.triggered.connect(self.saveFile)
        exit_action.triggered.connect(self.exit)

        colors = c1, c2, c3, c4, c5, c6 = (QColor(randint(0, 255),
                                                  randint(0, 255),
                                                  randint(0, 255))
                                           for _ in range(6))
        self.toolbar = self.addToolBar("Toolbar")
        pallettes = p1, p2, p3, p4, p5, p6 = (QAction(self)
                                              for _ in range(6))

        for color, pallette in zip(colors, pallettes):
            pallette.setStyleSheet("QPushButton{background-color:{color}}"
                                   .format(color=color))
            pallette.clicked.connect(lambda: self.mixColor)
            self.toolbar.addAction(pallette)

        self.pointy_pen = Tool("Pointy Pen", randint(0, 10), 1, Qt.black,
                               [randint(1, 4), randint(1, 2), randint(0, 3),
                                randint(0, 5)], self,
                               "Design/icons/Pointy Pen.png",
                               "CTRL+P", "A very pointy pen"
                               )

        self.fill = Tool("A bucket", 1, 2000, Qt.black,
                         [1, 1, 1, 1], self,
                         'Design/icons/A bucket.png',
                         "CTRL+B", "A bucket"
                         )

        self.straggly_paintbrush = Tool("Straggly Paintbrush", randint(0, 10),
                                        10, Qt.black,
                                        [randint(1, 4), randint(1, 2),
                                         randint(0, 3), randint(0, 5)],
                                        self,
                                        "Design/icons/Straggly Paintbrush.png",
                                        "CTRL+A", "A very Straggly Paintbrush."
                                        )

        self.solidifed_brush = Tool("Solid Brush", 1, 10, Qt.black,
                                    [randint(1, 4), randint(1, 2),
                                     randint(0, 3), randint(0, 5)], self,
                                    'Design/icons/Solid Brush.png',
                                    "CTRL+J", "Gosh, that is a hard tip"
                                    )

        self.show()

        self.drawing = False
        self.lastPoint = QPoint()

    def changePaintBoardVars(self, curToolName=None,
                             curBrushsize=1, curBrushColor=Qt.black,
                             curPaintPattern=0, curDuration=5):
        # print("hey from inside changePaintBoardVars.
        # These are my args:
        # Toolname: {},
        # Brushsize: {},
        # Brushcolor: {},
        # Paintpattern: {}".format(curToolName,
        #                   curBrushsize,
        #                   curBrushColor,
        #                   curPaintPattern))
        self.currentToolName = curToolName
        self.currentBrushSize = curBrushsize
        self.currentPaintPattern = curPaintPattern
        self.currentBrushColor = curBrushColor
        self.currentToolDuration = curDuration

        self.setCursor(QCursor(
            QPixmap("Design/icons/{}.png".format(self.currentToolName
                                                 if self.currentToolName
                                                 else None
                                                 ))))

    def mix_color(self, pallette, tool):
        if tool.toolName in ["A bucket", "Straggly Paintbrush"
                             "Solid Brush"]:
            # tool[r,b,g]
            if not ((tool.color[0] and tool.color[1]
                     and tool.color[2]) and self.t):
                tool.color = pallette.QColor
            else:  # perhaps don't divide by 4
                mixedColor = QColor(
                    pallette[0] - (max(pallette[0], tool.color[0] // 4) -
                                   min(pallette[0], tool.color[0] // 4)),
                    pallette[1] - (max(pallette[1], tool.color[1] // 4) -
                                   min(pallette[1], tool.color[1] // 4)),
                    pallette[2] - (max(pallette[2], tool.color[2] // 4) -
                                   min(pallette[2], tool.color[2] // 4)),
                    255
                )
                pallette.QColor, tool.color = mixedColor, mixedColor
                tool.isDipped = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.canvas)
            Pen = QPen()
            if self.currentToolDuration <= 0.0:
                print('Tools Died')
                self.currentToolDuration = 0
                Pen.setDashPattern([0, 0, 0, 0])
                self.drawing = False
            else:
                self.currentToolDuration -= 0.01
                print(self.currentToolDuration)

            if self.currentToolDuration < 1.5:
                size_of_dashes = self.currentPaintPattern
                Pen.setDashPattern(size_of_dashes)

            Pen.setColor(self.currentBrushColor)
            Pen.setWidth(self.currentBrushSize)
            if self.currentToolName == "Pointy Pen":
                Pen.setCapStyle(Qt.RoundCap)
                Pen.setJoinStyle(Qt.BevelJoin)
            elif self.currentToolName == "Straggly Paintbrush" or\
                    "Solid Brush":
                Pen.setCapStyle(Qt.SquareCap)
                Pen.setJoinStyle(Qt.MiterJoin)
            painter.setPen(Pen)
            if event.pos().y() > 53 and self.currentToolName is not None:
                painter.drawLine(self.lastPoint, event.pos())
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
