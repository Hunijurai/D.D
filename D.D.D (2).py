import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 100
        width = 1300
        height = 900

        self.setWindowTitle('D.D.D.')
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QtGui.QIcon('main.png'))

        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.white)

        self.pen = True
        self.point = False
        self.spray = False
        self.brushSize = 3
        self.brushColor = QtCore.Qt.black

        self.lastPoint = QtCore.QPoint()

        menu_items = {'File': [{'name': 'Save', 'icon': 'save.png', 's_cut': "Ctrl+S", 'act': self.save},
                               {'name': 'Clear', 'icon': 'clear.png', 's_cut': "Ctrl+C", 'act': self.clear}],
                      'Brush Size': [{'name': '3x', 'icon': 'three.png', 's_cut': "1", 'act': self.threex},
                                     {'name': '5x', 'icon': 'five.png', 's_cut': "2", 'act': self.fivex},
                                     {'name': '7x', 'icon': 'seven.png', 's_cut': "3", 'act': self.sevenx},
                                     {'name': '9x', 'icon': 'ten.png', 's_cut': "4", 'act': self.tenx},
                                     {'name': '20x', 'icon': 'twenty.png', 's_cut': "5", 'act': self.twentyx}
                                     ],
                      'Brush Color': [{'name': 'Black', 'icon': 'black.png', 's_cut': "Ctrl+B", 'act': self.black},
                                      {'name': 'Red', 'icon': 'red.png', 's_cut': "Ctrl+R", 'act': self.red},
                                      {'name': 'Green', 'icon': 'green.png', 's_cut': "Ctrl+G", 'act': self.green},
                                      {'name': 'Yellow', 'icon': 'yellow.png', 's_cut': "Ctrl+Y", 'act': self.yellow},
                                      {'name': 'White', 'icon': 'white.png', 's_cut': "Ctrl+W", 'act': self.white}
                                      ],
                      'Brush Styles': [{'name': 'Pen', 'icon': 'line.png', 's_cut': '', 'act': self.pen1},
                                       {'name': 'point', 'icon': 'Dotline.png', 's_cut': '', 'act': self.point1},
                                       {'name': 'spray', 'icon': 'spray.png', 's_cut': '', 'act': self.spray1}
                                       ]
                      }

        self.build_menu(menu_items)

    def build_menu(self, menu_dict):
        menu_bar = self.menuBar()
        for menu in menu_dict.keys():
            menu_list = menu_bar.addMenu(menu)
            for menu_item in menu_dict[menu]:
                this_menu_item = QtWidgets.QAction(QtGui.QIcon(menu_item['icon']), menu_item['name'], self)
                this_menu_item.setShortcut(menu_item['s_cut'])
                menu_list.addAction(this_menu_item)
                this_menu_item.triggered.connect(menu_item['act'])

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton) & self.point:
            painter = QtGui.QPainter(self.image)

            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))

            painter.drawPoint(event.pos())

            self.lastPoint = event.pos()
            self.update()

        elif (event.buttons() & QtCore.Qt.LeftButton) & self.pen:
            painter = QtGui.QPainter(self.image)
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

        elif (event.buttons() & QtCore.Qt.LeftButton) & self.spray:
            painter = QtGui.QPainter(self.image)
            painter.setPen(QtGui.QPen(self.brushColor, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap,
                                      QtCore.Qt.RoundJoin))

            for _ in range(20 * self.brushSize):
                xo = random.gauss(0, self.brushSize)
                yo = random.gauss(0, self.brushSize)
                painter.drawPoint(event.x() + xo, event.y() + yo)

        self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.update()

    def paintEvent(self, event):
        canvas_painter = QtGui.QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.image.rect())

    def pen1(self):
        self.pen = True
        self.spray = False
        self.point = False

    def spray1(self):
        self.spray = True
        self.pen = False
        self.point = False

    def point1(self):
        self.point = True
        self.spray = False
        self.pen = False

    def save(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg;;ALL Files(*.*)")
        if file_path == "":
            return
        self.image.save(file_path)

    def clear(self):
        self.image.fill(QtCore.Qt.white)
        self.update()

    def threex(self):
        self.brushSize = 3

    def fivex(self):
        self.brushSize = 5

    def sevenx(self):
        self.brushSize = 7

    def tenx(self):
        self.brushSize = 10

    def twentyx(self):
        self.brushSize = 20

    def black(self):
        self.brushColor = QtCore.Qt.black

    def red(self):
        self.brushColor = QtCore.Qt.red

    def green(self):
        self.brushColor = QtCore.Qt.green

    def yellow(self):
        self.brushColor = QtCore.Qt.yellow

    def white(self):
        self.brushColor = QtCore.Qt.white


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
