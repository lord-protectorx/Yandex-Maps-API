import sys
import os
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт
import requests
import PyQt5
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic



class Api(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Api.ui', self)
        self.searchButton.clicked.connect(self.initUI)


    def initUI(self):
        self.lat = self.latEdit.text()
        self.lon = self.lonEdit.text()
        self.delta = "0.005"
        self.api_server = "http://static-maps.yandex.ru/1.x/"

        self.params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([self.delta, self.delta]),
            "l": "map"
        }

        self.create_image()


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



        # self.image = QPixmap()
        # self.image.loadFromData(self.response.content)
        # return self.image


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Api()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


