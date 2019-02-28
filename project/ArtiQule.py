import sys
from random import randint
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtWidgets import (QMainWindow, QApplication,
                             QAction, QFileDialog, QPushButton,
                             QToolBox, QSizePolicy, QToolButton)
from PyQt5.QtGui import (QImage, QPainter, QPen, QPixmap,
                         QIcon, QCursor, QColor, QBrush)

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

        self.pointy_pen = {
            "toolName": "pointy_pen",
            "duration": randint(0,10),
            "brushSize": 1,
            "color":Qt.black,
            "paintPattern": Qt.SolidLine

        }
        pointy_pen_btn = QAction(QIcon('Design/icons/pointy_pen.png'),
                                 "Pointy Pen", self)
        pointy_pen_btn.setShortcut("CTRL+P")
        pointy_pen_btn.setStatusTip("A very pointy pen")
        pointy_pen_btn.triggered.connect(lambda :self.changePaintBoardVars(
            self.pointy_pen["toolName"],
            self.pointy_pen["brushSize"],
            self.pointy_pen["paintPattern"],
            self.pointy_pen["color"]
        ))

        self.fill = {
            "toolName": "fill_empty",
            "duration": 1,
            "brushSize": 50,
            "color": None,
            "paintPattern": "big dump",  #TODO: Custom pattern
            "is_dipped": False
        }
        fill_btn = QAction(QIcon('Design/icons/fill_empty.png'),
                           "A bucket", self)
        fill_btn.setShortcut("CTRL+P")
        fill_btn.setStatusTip("A bucket.")
        fill_btn.triggered.connect(lambda: self.changePaintBoardVars(
            self.fill["toolName"],
            self.fill["brushSize"],
            self.fill["color"],
            self.fill["paintPattern"]
        ))

        self.straggly_paintbrush = {
            "toolName": "straggly_paintbrush",
            "duration": randint(10,30),
            "brushSize": 10,
            "color": None,
            "paintPattern": "spread out pattern",  # TODO: Custom pattern
            "is_dipped": False

        }
        straggly_paintbrush_btn = QAction(QIcon(
                             'Design/icons/straggly_paintbrush.png'),
                                          "Straggly Paintbrush", self)
        straggly_paintbrush_btn.setShortcut("CTRL+A")
        straggly_paintbrush_btn.setStatusTip("A very Straggly Paintbrush.")
        straggly_paintbrush_btn.triggered.connect(lambda: self.changePaintBoardVars(
            self.straggly_paintbrush["toolName"],
            self.straggly_paintbrush["brushSize"],
            self.straggly_paintbrush["color"],
            self.straggly_paintbrush["paintPattern"]
        ))

        self.solidifed_brush = {
            "toolName": "solidified_brush",
            "duration": 1,
            "brushSize": 50,
            "paintPattern": "hit with a brick",  # TODO: Custom pattern
            "color": self.currentBrushColor,
            "is_dipped": False
        }
        solidified_brush_btn = QAction(QIcon(
                               'Design/icons/solidified_brush.png'),
                                        "A solid brush", self)
        solidified_brush_btn.setShortcut("CTRL+A")
        solidified_brush_btn.setStatusTip("Gorsh, that is a hard tip")
        solidified_brush_btn.triggered.connect(lambda: self.changePaintBoardVars(
            self.solidifed_brush["toolName"],
            self.solidifed_brush["brushSize"],
            self.solidifed_brush["color"],
            self.solidifed_brush["paintPattern"]
        ))

        colors = c1, c2, c3, c4, c5, c6 = (QColor(randint(0,255),
                                                  randint(0,255),
                                                  randint(0,255))
                                           for _ in range(6))
        self.toolbar = self.addToolBar("Toolbar")
        pallettes = p1, p2, p3, p4, p5, p6 = (QAction(self)
                                              for _ in range(6))

        self.toolbar.addAction(pointy_pen_btn)
        self.toolbar.addAction(fill_btn)
        self.toolbar.addAction(straggly_paintbrush_btn)
        self.toolbar.addAction(solidified_brush_btn)

        for color, pallette in zip(colors, pallettes):
            pallette.setStyleSheet("QPushButton{background-color:{color}}"\
                                   .format(color=color))
            pallette.clicked.connect(lambda: self.mixColor)
            self.toolbar.addAction(pallette)

        self.show()

        self.drawing = False
        self.lastPoint = QPoint()

    def changePaintBoardVars(self, curToolName=None,
        curBrushsize=1, curBrushColor=None, curPaintPattern=Qt.SolidLine):
        self.currentToolName = curToolName
        self.currentBrushSize = curBrushsize
        self.currentPaintPattern = curPaintPattern
        self.currentBrushColor = curBrushColor

        self.setCursor(QCursor(
            QPixmap("Design/icons/{}.png".format(self.currentToolName
                                                 if self.currentToolName
                                                 else None
                                                 ))))

    def mix_color(self, pallette, tool):
        if tool["toolName"] in ["fill_empty","straggly_paintbrush"
                                "solidified_brush"]:
                   #r             #g          #b
            if not ((tool[0] and tool[1] and tool[2]) and self.t):
                tool["color"] = pallette.QColor
            else:  # perhaps don't divide by 4
                mixedColor = QColor(
                    pallette[0] - (max(pallette[0], tool[0] // 4) -
                              min(pallette[0], tool[0] // 4)),
                    pallette[1] - (max(pallette[1], tool[1] // 4) -
                              min(pallette[1], tool[1] // 4)),
                    pallette[2] - (max(pallette[2], tool[2] // 4) -
                              min(pallette[2], tool[2] // 4)),
                    255
                )
                pallette.QColor, tool["color"] = mixedColor, mixedColor
                tool["isDipped"] = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() and Qt.LeftButton) and self.drawing:
            painter = QPainter(self.canvas)
            painter.setPen(QPen(self.currentBrushColor, self.currentBrushSize,
                        self.currentPaintPattern, Qt.RoundCap, Qt.RoundJoin))
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
