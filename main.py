import json
import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtWidgets

SCREEN_SIZE = [600, 450]


class Ui_Map(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(732, 782)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.schemeButton = QtWidgets.QPushButton(Dialog)
        self.schemeButton.setObjectName("schemeButton")
        self.horizontalLayout_2.addWidget(self.schemeButton)
        self.satelliteButton = QtWidgets.QPushButton(Dialog)
        self.satelliteButton.setObjectName("satelliteButton")
        self.horizontalLayout_2.addWidget(self.satelliteButton)
        self.hybridButton = QtWidgets.QPushButton(Dialog)
        self.hybridButton.setObjectName("hybridButton")
        self.horizontalLayout_2.addWidget(self.hybridButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.image = QtWidgets.QLabel(Dialog)
        self.image.setObjectName("image")
        self.verticalLayout.addWidget(self.image)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.inputLineEdit = QtWidgets.QLineEdit(Dialog)
        self.inputLineEdit.setInputMask("")
        self.inputLineEdit.setText("")
        self.inputLineEdit.setClearButtonEnabled(False)
        self.inputLineEdit.setObjectName("inputLineEdit")
        self.horizontalLayout_4.addWidget(self.inputLineEdit)
        self.findButton = QtWidgets.QPushButton(Dialog)
        self.findButton.setObjectName("findButton")
        self.horizontalLayout_4.addWidget(self.findButton)
        self.resetButton = QtWidgets.QPushButton(Dialog)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout_4.addWidget(self.resetButton)
        self.horizontalLayout_4.setStretch(0, 4)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.adressLabel = QtWidgets.QLabel(Dialog)
        self.adressLabel.setText("")
        self.adressLabel.setObjectName("adressLabel")
        self.horizontalLayout_6.addWidget(self.adressLabel)
        self.indexButton = QtWidgets.QPushButton(Dialog)
        self.indexButton.setObjectName("indexButton")
        self.horizontalLayout_6.addWidget(self.indexButton)
        self.horizontalLayout_6.setStretch(0, 2)
        self.horizontalLayout_6.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.schemeButton.setText(_translate("Dialog", "Схема"))
        self.satelliteButton.setText(_translate("Dialog", "Спутник"))
        self.hybridButton.setText(_translate("Dialog", "Гибрид"))
        self.image.setText(_translate("Dialog", "TextLabel"))
        self.inputLineEdit.setPlaceholderText(_translate("Dialog", "Введите адрес"))
        self.findButton.setText(_translate("Dialog", "Искать"))
        self.resetButton.setText(_translate("Dialog", "Сбросить"))
        self.indexButton.setText(_translate("Dialog", "Вкл/выкл почтовый индекс"))


def static_api(coords, scale, layer, point):
    if point:
        pt = f'{",".join(point)},pm2gnl'
    else:
        pt = ''
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join(coords),
        "z": scale,
        "l": layer,
        'pt': pt
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
        self.layer = 'map'
        self.point = ''
        self.setupUi(self)
        self.getImage()
        self.initUI()

    def getImage(self):
        response = static_api(self.coords, self.scale, self.layer, self.point)

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

        self.satelliteButton.clicked.connect(self.change_layer)
        self.schemeButton.clicked.connect(self.change_layer)
        self.hybridButton.clicked.connect(self.change_layer)

        self.findButton.clicked.connect(self.find_object)
        self.resetButton.clicked.connect(self.reset_point)

    def reset_point(self):
        self.point = ''
        self.getImage()
        self.show_image()

    def find_object(self):
        request = geocoder_find(self.inputLineEdit.text())
        try:
            json_request = request.json()
            self.coords = json_request["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]['Point']['pos'].split(' ')
            self.point = json_request["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]['Point']['pos'].split(' ')
            self.getImage()
            self.show_image()
        except Exception:
            self.inputLineEdit.setText('Объект не найден')

    def change_layer(self, button):
        if self.sender() == self.satelliteButton:
            self.layer = 'sat'
        elif self.sender() == self.schemeButton:
            self.layer = 'map'
        else:
            self.layer = 'sat,skl'
        self.getImage()
        self.show_image()

    def keyPressEvent(self, event):
        self.inputLineEdit.clearFocus()
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
