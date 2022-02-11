import sys
import os
try:
    import requests
except:
    os.system("pip3 install requests")
    import requests
try:
    import PyQt5
except:
    os.system("pip3 install PyQt5")
    import PyQt5

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5 import QtCore


class Api(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Api.ui', self)

        self.lib = ['map', 'sat', 'sat,skl']
        self.counter = 0
        self.l = self.lib[0]
        self.delta = 17

        self.searchButton.clicked.connect(self.initUI)
        self.searchButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.latEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lonEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.modeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.modeButton.clicked.connect(self.modes)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)



    def initUI(self):
        self.lat = self.latEdit.text()
        self.lon = self.lonEdit.text()
        self.api_server = "http://static-maps.yandex.ru/1.x/"

        print(self.l)
        self.params = {
            "ll": ",".join([self.lon, self.lat]),
            "z": self.delta,
            "l": self.l
        }

        self.create_image()


    def modes(self):
        self.counter += 1
        if self.counter > 2: self.counter = 0
        self.l = self.lib[self.counter]

        self.initUI()


    def create_image(self):
        self.response = requests.get(self.api_server, params=self.params)
        if not self.response:
            # обработка ошибочной ситуации
            print('ПРобелма')

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        # PgDown
        if event.key() == Qt.Key_PageDown:
            self.delta -= 1
            self.params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": self.delta,
                "l": self.l
            }
        #PgUp
        if event.key() == Qt.Key_PageUp:
            self.delta += 1
            self.params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": self.delta,
                "l": self.l
            }
        # Up
        if event.key() == PyQt5.QtCore.Qt.Key_Up:
            self.lat = str(float(self.lat) + 1)
            self.params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": self.delta,
                "l": self.l
            }
        # Down
        if event.key() == Qt.Key_Down:
            self.lat = str(float(self.lat) - 1)
            self.params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": self.delta,
                "l": self.l
            }
        # Right
        if event.key() == Qt.Key_Right:
            self.lon = str(float(self.lon) + 1)
            self.params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": self.delta,
                "l": self.l
            }

        # Left
        if event.key() == Qt.Key_Left:
            self.lon = str(float(self.lon) - 1)
            self.params = {
                "ll": ",".join([self.lon, self.lat]),
                "z": self.delta,
                "l": self.l
            }

        self.create_image()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Api()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


