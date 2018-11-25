from PyQt5 import uic
import sys
from PyQt5.Qt import QTest, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QMimeData, QSize
import CoordenadasGet
import CiudadesGet
import TwitterGet
from operator import attrgetter
from logging import Logger, StreamHandler, Formatter, INFO, DEBUG, basicConfig
from datetime import datetime
import webbrowser

sheet = uic.loadUiType('SheetGetter.ui')
country = uic.loadUiType('Mostrar_Paises.ui')
display = uic.loadUiType('Twitter.ui')


class Sheet(sheet[0], sheet[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setObjectName('main')
        self.setStyleSheet(
            "#main {background-image: url(Twitter.jpg); background-attachment: fixed;}    ")
        self.pushButton.clicked.connect(self.get_city)
        self.apretaron1 = False

    def get_city(self):
        print('En Proceso de "La Experiencia')
        self.link = self.lineEdit.text()
        # NamedTuples con la información de los paises
        self.named_tuples = CiudadesGet.main(self.link)
        # Ahora tengo que mostrar los named_tuples
        self.hide()
        self.c = Country(self.link)
        self.c.show()


class Country(country[0], country[1]):
    def __init__(self, link):
        super().__init__()
        self.setupUi(self)
        self.setObjectName('main')
        self.setStyleSheet(
            "#main {background-image: url(Twitter.jpg); background-attachment: fixed;}    ")
        self.link = link
        self.paises = [i.pais for i in sheet.named_tuples]
        # Por terminos de tiempo no pude hacer que los paises sean infinitos
        # Pero los limitamos a los primeros 20 de la sheet
        for i in self.paises:
            pais = QLabel()
            pais.setMaximumWidth(300)
            pais.setStyleSheet(
                "QLabel { text-align: center; font-size: 16px; font-weight: bold}")
            pais.setText(i)
            self.caja_paises.addWidget(pais)
        self.pushButton.clicked.connect(self.apretaron)
        self.show()

    def apretaron(self):
        print('intento entrar al botón')
        if not sheet.apretaron1:
            pais = self.lineEdit2.text()
            if pais in self.paises:
                self.lineEdit2.setText("")
                sheet.apretaron1 = True
                for i in reversed(range(self.caja_paises.count())):
                    self.caja_paises.itemAt(i).widget().setParent(None)
                pos = self.paises.index(pais)
                self.ciudades = sheet.named_tuples[pos].ciudades
                for i in self.ciudades:
                    ciudad = QLabel()
                    ciudad.setMaximumWidth(300)
                    ciudad.setStyleSheet(
                        "QLabel { text-align: center; font-size: 16px; font-weight: bold}")
                    ciudad.setText(i)
                    self.caja_paises.addWidget(ciudad)
            else:
                print('No existe ese pais en la lista')
        else:
            self.apretaron2()

    def apretaron2(self):
        self.ciudad = self.lineEdit2.text()
        # La interfaz gráfica solo soporta 20 ciudades por país
        # Podía hacer un boxWidget, o hacerlo en html como hice los tweets
        # pero estoy en nivel -10 para el resto de mis examenes :(
        if self.ciudad in self.ciudades:
            self.coordenadas = CoordenadasGet.get_coordenadas(self.ciudad)
            self.a = DisplayTwitter(self.ciudad, self.coordenadas, self.link)
            if self.coordenadas == None:
                self.a.logger.error(
                    "Error de localización: La localización no existe")
                CiudadesGet.append_to_sheet_logger(self.link,
                                                   [datetime.utcnow(),
                                                    '[Error]',
                                                    "Error de localización: La localización no existe"])
            else:
                self.a.hacer_todo(self.ciudad)
                self.a.show()
                self.hide()
        else:
            print('Esa ciudad no está en lista')


class DisplayTwitter(display[0], display[1]):
    def __init__(self, ciudad, coordenadas, link):
        super().__init__()
        self.setupUi(self)
        self.setObjectName('main')
        self.setStyleSheet(
            "#main {background-image: url(Twitter.jpg); background-attachment: fixed;}    ")
        self.link = link
        self.logger = Logger("Pro Twitter")
        self.logger.setLevel(INFO)
        self.archivo = open('logger.txt', 'a')
        self.formater = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.sh = StreamHandler(self.archivo)
        self.sh.setLevel(DEBUG)
        self.sh.setFormatter(self.formater)
        self.shc = StreamHandler()
        self.shc.setLevel(DEBUG)
        self.shc.setFormatter(self.formater)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.shc)
        self.coordenadas = coordenadas

    def hacer_todo(self, ciudad):
        trending = TwitterGet.datos_twitter(self.coordenadas)
        self.main.setText('Tweets de {}'.format(ciudad))
        self.main.setStyleSheet('font-size: 24px; font-weight: bold;')
        self.topic1.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold}")
        self.topic1.setText('N°1 - ' + trending[0][0])
        self.topic2.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold}")
        self.topic2.setText('N°2 - ' + trending[1][0])
        self.topic3.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold}")
        self.topic3.setText('N°3 - ' + trending[2][0])
        self.topic4.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold}")
        self.topic4.setText('N°4 - ' + trending[3][0])
        self.topic5.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold}")
        self.topic5.setText('N°5 - ' + trending[4][0])
        tweets_varios = TwitterGet.get_twiteros(self.coordenadas)
        if len(tweets_varios) == 0:
            self.logger.error("Error de Tweet: No se encontró ningun Tweet.")
            # Aprendí que se podía usar mas de 1 handler y que podía
            # pasarlo directo al Sheets, pero por la misma razón de antes D:
            CiudadesGet.append_to_sheet_logger(self.link,
                                               [datetime.utcnow(), '[Error]',
                                                "Error de Tweet: No se encontró ningun Tweet."])

        if len(tweets_varios) < 20:
            self.logger.warning(
                "Alerta de Tweet: Hay menos de 20 Tweets en la zona.")
            CiudadesGet.append_to_sheet_logger(self.link,
                                               [datetime.utcnow(), '[Warning]',
                                                "Alerta de Tweet: Hay menos de 20 Tweets en la zona."])

        if len(tweets_varios) == 20:
            self.logger.info(
                "Busqueda Exitosa: La consulta funcionó correctamente.")
            CiudadesGet.append_to_sheet_logger(self.link,
                                               [datetime.utcnow(), "[Info]",
                                                "Busqueda Exitosa: La consulta funcionó correctamente."])

        tweets_varios = sorted(tweets_varios, key=attrgetter('followers'))
        tweets_varios.reverse()
        html = []
        for i in tweets_varios:
            html.append((
                '<html><h4 style="color:blue;"> <pre></pre> '
                'Followers: {f} <pre></pre> '
                'Usuario: {u} <pre></pre> '
                'Tweet: {t}<pre></pre></h4></html>').format(
                f=i.followers, u=i.usuario, t=i.tweet))

        html = "".join(html)
        self.Caja_Tweets.setHtml(html)

        self.LinkSheets.clicked.connect(self.ir_al_link)

    def ir_al_link(self):
        webbrowser.open(self.link)


if __name__ == '__main__':
    app = QApplication([])
    sheet = Sheet()
    sheet.show()
    sys.exit(app.exec_())
