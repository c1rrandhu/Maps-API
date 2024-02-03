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
        self.spn.setText('1')
        self.button.clicked.connect(self.confirm)
        self.reset_button.clicked.connect(self.reset)

    def reset(self):
        self.lon.clear()
        self.lat.clear()
        self.spn.clear()

    def confirm(self):
        self.map_zoom = int(self.spn.text())
        self.ll = [float(self.lon.text()), float(self.lat.text())]
        self.setMap()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_PageUp and self.map_zoom < 17:
            self.map_zoom += 1
        if key == Qt.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if key == Qt.Key_Left:
            self.ll[0] -= 0.01 * self.map_zoom
        if key == Qt.Key_Right:
            self.ll[0] += 0.01 * self.map_zoom
        if key == Qt.Key_Up:
            self.ll[1] += 0.01 * self.map_zoom
        if key == Qt.Key_Down:
            self.ll[1] -= 0.01 * self.map_zoom

        self.setMap()

    def setMap(self):
        longitude = str(self.ll[0])
        latitude = str(self.ll[1])

        params = {'ll': ",".join([longitude, latitude]),
                  'l': 'map',
                  'z': self.map_zoom}
        response = requests.get(f'http://static-maps.yandex.ru/1.x/', params=params)

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)
        pixmap = QPixmap()
        pixmap.load('tmp.png')

        self.map_label.setPixmap(pixmap)
        os.remove('tmp.png')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
    print(1)
