import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Maps-API')

        self.lon.setText('37.977751')
        self.lat.setText('55.757718')
        self.spn.setText('15')

        self.l = 'map'
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        # self.map_zoom = int(self.spn.text())
        # self.ll = [float(self.lon.text()), float(self.lat.text())]
        self.setMap()

    def setMap(self):
        params = {'ll': ",".join([str(float(self.lon.text())), str(float(self.lat.text()))]),
                  'l': self.l,
                  'z': int(self.spn.text())}
        response = requests.get(f'http://static-maps.yandex.ru/1.x/', params=params)

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        self.mapwindow = MapWindow()
        self.mapwindow.show()


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.temp = MainWindow()
        self.ll = [float(self.temp.lon.text()), float(self.temp.lat.text())]
        self.l = 'map'
        self.map_zoom = int(self.temp.spn.text())

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.map_lbl.setPixmap(pixmap)
        os.remove('tmp.png')

    def keyPressEvent(self, event):
        key = event.key()

        if (event.key() == Qt.Key_Plus) and QApplication.keyboardModifiers() == Qt.ShiftModifier and self.map_zoom < 17:
            self.map_zoom += 1
        elif (event.key() == Qt.Key_Minus) and QApplication.keyboardModifiers() == Qt.AltModifier and self.map_zoom > 0:
            self.map_zoom -= 1
        elif key == Qt.Key_Left:
            self.ll[0] -= 0.001 * self.map_zoom
        elif key == Qt.Key_Right:
            self.ll[0] += 0.001 * self.map_zoom
        elif key == Qt.Key_Up:
            self.ll[1] += 0.001 * self.map_zoom
        elif key == Qt.Key_Down:
            self.ll[1] -= 0.001 * self.map_zoom
        elif key == Qt.Key_0:
            if self.l == 'map':
                self.l = 'sat'
            else:
                self.l = 'map'

        self.change()

    def change(self):
        params = {'ll': ",".join([str(float(self.ll[0])), str(float(self.ll[1]))]),
                  'l': self.l,
                  'z': int(self.map_zoom)}
        response = requests.get(f'http://static-maps.yandex.ru/1.x/', params=params)

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.map_lbl.setPixmap(pixmap)
        os.remove('tmp.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
