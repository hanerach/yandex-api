import json
import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets


SCREEN_SIZE = [600, 450]


class Ui_Map(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1015, 870)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.image = QtWidgets.QLabel(Dialog)
        self.image.setObjectName("image")
        self.verticalLayout.addWidget(self.image)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.satelliteRb = QtWidgets.QRadioButton(Dialog)
        self.satelliteRb.setObjectName("satelliteRb")
        self.LayersBtnGroup = QtWidgets.QButtonGroup(Dialog)
        self.LayersBtnGroup.setObjectName("LayersBtnGroup")
        self.LayersBtnGroup.addButton(self.satelliteRb)
        self.horizontalLayout_2.addWidget(self.satelliteRb)
        self.hybridRb = QtWidgets.QRadioButton(Dialog)
        self.hybridRb.setObjectName("hybridRb")
        self.LayersBtnGroup.addButton(self.hybridRb)
        self.horizontalLayout_2.addWidget(self.hybridRb)
        self.schemeRb = QtWidgets.QRadioButton(Dialog)
        self.schemeRb.setObjectName("schemeRb")
        self.LayersBtnGroup.addButton(self.schemeRb)
        self.horizontalLayout_2.addWidget(self.schemeRb)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 6)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.satelliteRb.setChecked(True)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.image.setText(_translate("Dialog", "TextLabel"))
        self.satelliteRb.setText(_translate("Dialog", "Спутник"))
        self.hybridRb.setText(_translate("Dialog", "Гибрид"))
        self.schemeRb.setText(_translate("Dialog", "Схема"))


def static_api(response, scale):
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "z": scale,
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    return requests.get(map_api_server, params=map_params)


def geocoder_find(toponym_to_find):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    # print(geocoder_api_server + )
    qqq = requests.get(geocoder_api_server, params=geocoder_params)
    return qqq


def json_file(response):
    file = open('first_json.json', 'w', encoding='utf8')
    json.dump(response.json(), file, ensure_ascii=False, indent=4)
    file.close()


class Example(QWidget, Ui_Map):
    def __init__(self):
        super().__init__()
        self.scale = '10'
        self.coords = ['37.22093', '55.99799']
        self.setupUi(self)
        self.getImage()
        self.initUI()

    def getImage(self):
        geocoder = geocoder_find(','.join(self.coords))
        response = static_api(geocoder, self.scale)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def show_image(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.show_image()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.scale = str(int(self.scale) + 1)
        if event.key() == Qt.Key_PageDown:
            self.scale = str(int(self.scale) - 1)
        if event.key() == Qt.Key_Right:
            self.coords[0] = str(float(self.coords[0]) + 0.1)
        if event.key() == Qt.Key_Up:
            self.coords[1] = str(float(self.coords[1]) + 0.1)
        if event.key() == Qt.Key_Down:
            self.coords[1] = str(float(self.coords[1]) - 0.1)
        if event.key() == Qt.Key_Left:
            self.coords[0] = str(float(self.coords[0]) - 0.1)
        self.getImage()
        self.show_image()



    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def change_scale(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())