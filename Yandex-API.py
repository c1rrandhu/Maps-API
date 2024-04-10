import os
import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Maps-API')

        self.lon.setText('37.977751')
        self.lat.setText('55.757718')
        self.spn.setText('15')
        self.address_input.setText('г. Москва, ул. Барклая, 5А')

        self.l = 'map'
        self.button.clicked.connect(self.confirm_1)
        self.address_btn.clicked.connect(self.confirm_2)

    def confirm_1(self):
        self.setMap()

    def confirm_2(self):
        self.set_precised_map()

    def set_precised_map(self):
        geocoder = (f'http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&'
                    f'geocode={self.address_input.text()}&format=json')
        response = requests.get(geocoder).json()['response']['GeoObjectCollection']['featureMember'][0]
        coords = response['GeoObject']['Point']['pos'].split()

        point = ','.join([str(float(coords[0])), str(float(coords[1]))])
        params = {'ll': point,
                  'l': self.l,
                  'z': 15,
                  'pt': point + ',flag'}
        response = requests.get(f'http://static-maps.yandex.ru/1.x/', params=params)

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        self.map_window = MapWindow(point, 15, flag=True)
        self.map_window.show()

    def setMap(self):
        coords = ",".join([str(float(self.lon.text())), str(float(self.lat.text()))])
        spn = int(self.spn.text())
        params = {'ll': coords,
                  'l': self.l,
                  'z': spn}
        response = requests.get(f'http://static-maps.yandex.ru/1.x/', params=params)

        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        self.map_window = MapWindow(coords, spn)
        self.map_window.show()


class MapWindow(QMainWindow):
    def __init__(self, coords, spn, flag=False):
        super().__init__()
        uic.loadUi('map.ui', self)
        self.ll = list(map(float, coords.split(',')))
        self.init_ll = self.ll.copy()
        self.l = 'map'
        self.map_zoom = spn
        self.flag = flag

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.map_lbl.setPixmap(pixmap)
        os.remove('tmp.png')

        self.reset_btn.clicked.connect(self.reset_coord)

    def reset_coord(self):
        self.close()

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
        if self.flag:
            flag = ','.join(map(str, self.init_ll)) + ',flag'
        else:
            flag = ''
        params = {'ll': ','.join([str(float(self.ll[0])), str(float(self.ll[1]))]),
                  'l': self.l,
                  'z': int(self.map_zoom),
                  'pt': flag}
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
