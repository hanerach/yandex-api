import json
import os
import sys

import requests
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


def scale_finder(response):
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_lc = toponym['boundedBy']['Envelope']['lowerCorner'].split(' ')
    toponym_uc = toponym['boundedBy']['Envelope']['upperCorner'].split(' ')
    toponym_size_tuple = str(float(toponym_uc[0]) - float(toponym_lc[0])), str(
        float(toponym_uc[1]) - float(toponym_lc[1]))
    return list(toponym_size_tuple)


def static_api(response):
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    # Масштаб
    scale = scale_finder(response)

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(scale),
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


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        geocoder = geocoder_find('зеленоград корпус 314')
        response = static_api(geocoder)
        # if not response:
        #     print("Ошибка выполнения запроса:")
        #     print(map_request)
        #     print("Http статус:", response.status_code, "(", response.reason, ")")
        #     sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)


    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())