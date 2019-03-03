import sys
import time
from random import randint
from PyQt5.QtCore import QPoint, Qt, QThread, pyqtSignal
from PyQt5.QtGui import (QColor, QCursor, QIcon, QImage, QPainter,
                         QPen, QPixmap)
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog,
                             QMainWindow, QPushButton, )

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

SoundEffects = {
    'pen break': r'Sounds/pen break.mp3',
    'pen write': r'Sounds/pen writing.wav',
    'fill bucket': r'Sounds/fill bucket.mp3',
    'empty bucket': r'Sounds/empty bucket.mp3',
    'solid hitting': r'Sounds/solidified hitting.m4a',
    'straggly brush': r'Sounds/straggly brushing.m4a'
}


class ColorBox(QMainWindow):
    """ This window holds all the color pallettes"""
    objs = []

    def __init__(self, parent=None):
        super().__init__(parent)
        ColorBox.objs.append(self)
        self.toolsX = 5
        self.toolsY = 5
        self.tools_holder = 0
        self.exists = True
        self.Setup()
        # TODO MINOR: can open as many windows as one desires

    def Setup(self):
        # self.setGeometry(990, 150, 150, 300)
        self.setWindowTitle('Colorbox')
        self.setFixedSize(150, 300)

    def addPallette(self, pallet):
        pallet.setGeometry(self.toolsX, self.toolsY, 40, 40)
        self.layout().addWidget(pallet)
        self.toolsX += 50
        self.tools_holder += 1
        if self.tools_holder == 3:
            self.toolsX = 5
            self.toolsY += 50
            self.tools_holder = 0

    def showColorBox(self):
        self.show()

    def closeEvent(self, *args, **kwargs):
        self.exists = False

    @classmethod
    def setWindowCursor(cls, currentTool):
        """Connects Canvas window with colorBox window"""

        for obj in cls.objs:
            obj.setCursor(QCursor(QPixmap("Design/icons/{}.png".format(
                currentTool.toolName
                if currentTool else None)
            )
            )
            )


class Tool:
    def __init__(self, toolName, brushSize, color,
                 paintPattern, PaintBoard, iconPath, shortcut, statusTip,
                 duration, isDipped=False
                 ):
        """class for creating drawing tools

        Arguments:
            toolName {str} -- Tools name for display
            duration {tuple} -- randint duration[0], max time[1]
            constDuration {int} -- the tool's duration time
            brushSize {float} -- tools brushsize
            color {QColor} -- the Color to be used
            paintPattern {PaintPattern} -- the paint pattern that will be used
            PaintBoard {PaintBoard} -- Parent class
            iconPath {str} -- the path to the icon. duh...
            shortcut {str} -- well. its a shortcut. nothing less, nothing more.
            statusTip {str} -- the status tip that will be displayed...
        """

        self.toolName = toolName
        self.brushSize = brushSize
        self.color = color
        self.isDipped = isDipped
        self.paintPattern = paintPattern
        self.PaintBoard = PaintBoard
        self.iconPath = iconPath
        self.shortcut = shortcut
        self.statusTip = statusTip
        self.duration = duration[0]
        self.constDuration = duration[1]
        self.opacityDuration = 1

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
            lambda: self.PaintBoard.connectTool(
                self,
                curisDipped=self.isDipped
            )
        )
        self.PaintBoard.toolbar.addAction(tool_btn)


class PalletteButton:
    """Class for color pallete; allows for mixing colors"""

    def __init__(self, parentBtn):
        self.parentBtn = parentBtn
        self.r = randint(0, 255)
        self.g = randint(0, 255)
        self.b = randint(0, 255)
        self.alpha = 255
        self.palletteColor = self.r, self.g, self.b, self.alpha
        # {tuple} so it can be applied below
        self.timesToUse = randint(10, 20)
        # TODO: pallette will become empty after being used X amount of times

    def mixColor(self, tool):
        """Mixes colors from tool holding the color
           NO COLOR IN TOOL: Pick up color pallette color
               IS TOOL BUCKET: empties palette
           COLOR IN TOOL: Mix pallette and tool color;
               IS BUCKET: mixes
        """
        if tool is None or tool.toolName in \
                ("Pointy Pen", "Pointy Pen Broken", "Sunbathing Eraser"):
            return None

        if tool.toolName in ["A bucket", "Straggly PaintBrush",
                             "Solid Brush"]:
            colorSum = sum(
                [
                    tool.color.red(),
                    tool.color.green(),
                    tool.color.blue()
                ]
            )

            if colorSum and tool.color.alpha() and self.alpha:
                # self.alpha so that color pallette is not empty
                self.r = (self.r + tool.color.red()) // 2
                self.g = (self.g + tool.color.green()) // 2
                self.b = (self.b + tool.color.blue()) // 2
            elif tool.toolName == "A bucket filled":
                self.r = (self.r + tool.color.red()) // 4
                self.g = (self.g + tool.color.green()) // 4
                self.b = (self.b + tool.color.blue()) // 4
            elif not sum((self.r, self.g, self.b, self.alpha)):
                pass

            self.palletteColor = (self.r, self.g, self.b, self.alpha)
            tool.color = QColor(self.r, self.g, self.b, self.alpha)

            if tool.toolName == "Straggly PaintBrush" or "Solid Brush":
                tool.opacityDuration = 1
                tool.isDipped = True
            elif tool.toolName == "A bucket" and self.alpha:
                """The pallette gets emptied """
                self.r = 0
                self.g = 0
                self.b = 0
                self.alpha = 0
                self.palletteColor = (self.r, self.g,
                                      self.b, self.alpha)
                tool.toolName = "A bucket filled"
                tool.PaintBoard.connectTool(tool)
            tool.duration = randint(0, tool.constDuration)

        self.parentBtn.setStyleSheet(
            "background-color: rgba{0}; border-radius:20px".format(
                self.palletteColor
            )
        )


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
        self.connectTool()
        self.painter = QPainter(self.canvas)

        self.mousePos = QPoint(0, 0)

        # MENUBARS
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

        # TOOLBAR AND WITH TOOL ICONS

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.setStyleSheet('background-color: white')

        self.pointy_pen = Tool("Pointy Pen", 1, Qt.black,
                               [randint(1, 4), randint(1, 2), randint(0, 3),
                                randint(0, 5)], self,
                               "Design/icons/Pointy Pen.png",
                               "CTRL+P", "A very pointy pen",
                               (randint(1, 15), 15)
                               )

        # they shouldn't have any color in the beggining
        # alpha decrease -=1 ; tuple required
        self.fill = Tool("A bucket", 300, QColor(0, 0, 0, 0.0),
                         [1, 1, 1, 1], self,
                         'Design/icons/A bucket.png',
                         "CTRL+B", "A bucket",
                         (1, 1)
                         )

        self.straggly_paintbrush = Tool("Straggly PaintBrush",
                                        10, QColor(0, 0, 0, 0.0),
                                        [randint(1, 4), randint(1, 2),
                                         randint(0, 3), randint(0, 5)],
                                        self,
                                        "Design/icons/Straggly PaintBrush.png",
                                        "CTRL+A", "A Straggly PaintBrush.",
                                        (randint(5, 30), 30)  # randint(5,30)
                                        )

        self.solidifed_brush = Tool("Solid Brush", 10, QColor(0, 0, 0, 0.0),
                                    [randint(1, 4), randint(1, 2),
                                     randint(0, 3), randint(0, 5)], self,
                                    'Design/icons/Solid Brush.png',
                                    "CTRL+J", "Gosh, that is a hard tip",
                                    (1, 1)
                                    )

        self.sunbathing_eraser = Tool("Sunbathing Eraser", 10, Qt.white,
                                      [0, 0, 0, 0.0], self,
                                      "Design/icons/Sunbathing Eraser",
                                      "Ctrl+F",
                                      "Erase Your Mistakes, Kid!",
                                      (99999, 99999))  # infinte duration

        self.show()

        self.drawing = False
        self.lastPoint = QPoint()

    def connectTool(self, curTool=None, curisDipped=False):

        self.currentTool = curTool

        try:
            self.currentTool.duration
            self.currentTool.isDipped
        except AttributeError:
            pass
        else:
            self.currentTool.isDipped = curisDipped
            if self.currentTool.toolName == "Pointy Pen":
                self.currentTool.duration = randint(
                    0,
                    self.currentTool.constDuration
                )
        ColorBox.setWindowCursor(self.currentTool)

        self.setCursor(QCursor(
            QPixmap("Design/icons/{}.png".format(self.currentTool.toolName
                                                 if self.currentTool
                                                 else None
                                                 )
                    )))
        if self.currentTool is not None:
            if self.currentTool.toolName != \
                    "Pointy Pen" or \
                    "A bucket" or \
                    "Sunbathing Eraser" or \
                    "A bucket filled" \
                    and self.currentTool.isDipped:
                self.dripper = DripperEffect(
                    self.currentTool.color,
                    self.currentTool.brushSize
                )
                self.dripper.drip.connect(self.dripperHandler)
                self.dripper.start()

    def colorBoxRun(self):

        self.colorBox = ColorBox(self)
        ColorBox.setWindowCursor(self.currentTool)
        geo = self.geometry()
        geo.moveLeft(geo.right())  # moves window right
        self.colorBox.setGeometry(geo)

        p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16,\
        p17, p18 = (QPushButton() for _ in range(18))

        c1 = PalletteButton(p1)
        c2 = PalletteButton(p2)
        c3 = PalletteButton(p3)
        c4 = PalletteButton(p4)
        c5 = PalletteButton(p5)
        c6 = PalletteButton(p6)
        c7 = PalletteButton(p7)
        c8 = PalletteButton(p8)
        c9 = PalletteButton(p9)
        c10 = PalletteButton(p10)
        c11 = PalletteButton(p11)
        c12 = PalletteButton(p12)
        c13 = PalletteButton(p13)
        c14 = PalletteButton(p14)
        c15 = PalletteButton(p15)
        c16 = PalletteButton(p16)
        c17 = PalletteButton(p17)
        c18 = PalletteButton(p18)

        p1.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c1.palletteColor))
        p1.clicked.connect(lambda: c1.mixColor(self.currentTool))
        self.colorBox.addPallette(p1)
        p2.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c2.palletteColor))
        p2.clicked.connect(lambda: c2.mixColor(self.currentTool))
        self.colorBox.addPallette(p2)
        p3.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c3.palletteColor))
        p3.clicked.connect(lambda: c3.mixColor(self.currentTool))
        self.colorBox.addPallette(p3)
        p4.setStyleSheet("background-color: rgba{0}; border-radius:20px;"
                         .format(c4.palletteColor))
        p4.clicked.connect(lambda: c4.mixColor(self.currentTool))
        self.colorBox.addPallette(p4)
        p5.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c5.palletteColor))
        p5.clicked.connect(lambda: c5.mixColor(self.currentTool))
        self.colorBox.addPallette(p5)
        p6.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c6.palletteColor))
        p6.clicked.connect(lambda: c6.mixColor(self.currentTool))
        self.colorBox.addPallette(p6)
        p7.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c7.palletteColor))
        p7.clicked.connect(lambda: c7.mixColor(self.currentTool))
        self.colorBox.addPallette(p7)
        p8.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c8.palletteColor))
        p8.clicked.connect(lambda: c8.mixColor(self.currentTool))
        self.colorBox.addPallette(p8)
        p9.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                         .format(c9.palletteColor))
        p9.clicked.connect(lambda: c9.mixColor(self.currentTool))
        self.colorBox.addPallette(p9)
        p10.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c10.palletteColor))
        p10.clicked.connect(lambda: c10.mixColor(self.currentTool))
        self.colorBox.addPallette(p10)
        p11.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c11.palletteColor))
        p11.clicked.connect(lambda: c11.mixColor(self.currentTool))
        self.colorBox.addPallette(p11)
        p12.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c12.palletteColor))
        p12.clicked.connect(lambda: c12.mixColor(self.currentTool))
        self.colorBox.addPallette(p12)
        p13.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c13.palletteColor))
        p13.clicked.connect(lambda: c13.mixColor(self.currentTool))
        self.colorBox.addPallette(p13)
        p14.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c14.palletteColor))
        p14.clicked.connect(lambda: c14.mixColor(self.currentTool))
        self.colorBox.addPallette(p14)
        p15.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c15.palletteColor))
        p15.clicked.connect(lambda: c15.mixColor(self.currentTool))
        self.colorBox.addPallette(p15)
        p16.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c16.palletteColor))
        p16.clicked.connect(lambda: c16.mixColor(self.currentTool))
        self.colorBox.addPallette(p16)
        p17.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c17.palletteColor))
        p17.clicked.connect(lambda: c17.mixColor(self.currentTool))
        self.colorBox.addPallette(p17)
        p18.setStyleSheet("background-color: rgba{0}; border-radius:20px"
                          .format(c18.palletteColor))
        p18.clicked.connect(lambda: c18.mixColor(self.currentTool))
        self.colorBox.addPallette(p18)

        # showing toolBox
        self.colorBox.showColorBox()

    def dripperHandler(self, result):
        Dripper = result
        self.painter.setPen(Dripper)
        point = QPoint(self.cursor().pos().x(), self.cursor().pos().y())
        point = self.mapFromGlobal(point)
        self.painter.drawLine(point, point)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and \
                self.currentTool is not None:
            self.drawing = True
            if self.currentTool.toolName == "A bucket filled" \
                    and self.currentTool.duration >= 0:
                Pen = QPen()
                Pen.setColor(self.currentTool.color)
                Pen.setWidth(self.currentTool.brushSize)
                self.painter.setPen(Pen)
                self.painter.drawEllipse(event.pos(), 100, 150)
                self.currentTool.duration -= 1
                self.currentTool.toolName = "A bucket"
                self.currentTool.color = QColor(0, 0, 0, 0)
                self.connectTool(self.currentTool)

            self.lastPoint = event.pos()
            self.update()
        else:
            return None

    def mouseMoveEvent(self, event):
        self.mousePos = event.pos()
        if (event.buttons() and Qt.LeftButton) and \
                self.drawing and self.currentTool is not None:

            Pen = QPen()
            if self.currentTool.toolName != "Sunbathing Eraser":
                if self.currentTool.duration <= 0.0:
                    Pen.setDashPattern([0, 0, 0, 0])
                    self.drawing = False
                    self.dripper.stop()
                else:
                    self.currentTool.duration -= 0.1
                    if "Brush" in self.currentTool.toolName:
                        self.currentTool.opacityDuration -= 0.0125
                        # perhaps divide in class object

                # this here is to add more realism
                # to the point when its breaking
                if self.currentTool.duration <= 0.2:
                    dots = QPen()
                    broken_tools = QPen()
                    if self.currentTool.toolName == "Pointy Pen":
                        dots.setColor(Qt.black)
                        dots.setWidth(1)
                    if self.currentTool.toolName == "Solid Brush":
                        broken_tools.setColor(self.currentTool.color)
                        broken_tools.setCapStyle(Qt.SquareCap)
                        broken_tools.setJoinStyle(Qt.BevelJoin)
                        broken_tools.setWidth(self.currentTool.brushSize - 2)
                        self.painter.setPen(broken_tools)
                        self.painter.drawLine(self.lastPoint, self.lastPoint)
                    dots.setCapStyle(Qt.RoundCap)
                    dots.setJoinStyle(Qt.RoundJoin)
                    dots.setColor(self.currentTool.color)
                    dots.setDashPattern([25, 50, 25, 50])
                    dots.setStyle(Qt.DashDotDotLine)
                    self.painter.setPen(dots)
                    self.painter.drawLine(self.lastPoint +
                                          QPoint(randint(10, 15),
                                                 randint(1, 5)),
                                          self.lastPoint +
                                          QPoint(randint(5, 10),
                                                 randint(1, 10)))

                if self.currentTool.toolName == "Pointy Pen":
                    # QSound(SoundEffects['pen write']).play()
                    Pen.setCapStyle(Qt.RoundCap)
                    Pen.setJoinStyle(Qt.MiterJoin)
                elif self.currentTool.toolName == \
                        'Straggly Paintbrush' or 'Solid Brush':
                    if self.currentTool.toolName == "Solid Brush":
                        Pen.setCapStyle(Qt.RoundCap)
                        Pen.setJoinStyle(Qt.BevelJoin)
                    else:
                        Pen.setCapStyle(Qt.SquareCap)
                        Pen.setJoinStyle(Qt.MiterJoin)
                Pen.setColor(self.currentTool.color)
                Pen.setWidth(self.currentTool.brushSize)

                self.painter.setOpacity(self.currentTool.opacityDuration)
                self.painter.setPen(Pen)
                if self.currentTool.duration <= 0:
                    if self.currentTool.toolName == "Pointy Pen":
                        self.setCursor(QCursor(
                            QPixmap("Design/icons/Pointy Pen Broken.png")))
                        # QSound(SoundEffects['pen break']).play()

                self.painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()
            self.update()
        else:
            return None

    def mouseRealeaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(),
                                 self.canvas,
                                 self.canvas.rect()
                                 )

    def newCanvas(self):
        # TODO: Add New Canvas
        Pen = QPen()
        Pen.setWidth(5000)
        Pen.setColor(Qt.white)
        self.painter.setPen(Pen)
        self.painter.drawLine(0, 0, 1000, 500)
        self.update()

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


class DripperEffect(QThread):
    drip = pyqtSignal(object)

    def __init__(self, color, size):
        QThread.__init__(self)
        self.color = color
        self.size = size * 2
        print('size: ' + str(self.size))
        self._stop = False

    def stop(self):
        self._stop = True

    def run(self):
        while not self._stop:
            drip_chance = randint(0, 5)
            # 1/3 chance it drips
            if drip_chance < 2:
                Drip = QPen()
                Drip.setWidth(self.size)
                Drip.setStyle(Qt.DotLine)
                Drip.setColor(self.color)
                Drip.setJoinStyle(Qt.RoundJoin)
                Drip.setCapStyle(Qt.RoundCap)
                self.drip.emit(Drip)
                print('drip')
            else:
                pass
            time.sleep(0.5)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow{background-color:white}")
    myGUI = PaintBoard()

    sys.exit(app.exec_())
