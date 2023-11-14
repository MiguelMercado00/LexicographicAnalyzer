
import sys
import os
from ui_form import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import re

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.ui.btnPwd.clicked.connect(self.analizador_lexicografico)
        self.diccionario_reemplazo = {
            ":)": "png/003-feliz.png",
            ":(": "png/009-triste.png",
            ":D": "png/005-sonriente.png",
            ";)": "png/018-guino.png",
            ":P": "png/067-sacandolengua.png",
            "xD": "png/058-riendo.png",
            ":-)": "png/003-feliz.png",
            ":-(": "png/009-triste.png",
            "(y)": "png/028-pulgares-arriba.png",
            "(n)": "png/046-pulgares-abajo.png",
            "<3": "png/068-corazon.png",
            "\\m/": "png/069-manos-haciendo-el-signo-de-los-cuernos.png",
            ":-O": "png/004-conmocionado.png",
            ":O": "png/004-conmocionado.png",
            ":-|": "png/008-confuso.png",
            ":|": "png/008-confuso.png",
            ":*": "png/070-beso.png",
            ">:(": "png/035-enojado-1.png",
            "^^": "png/019-entusiasta.png",
            ":-]": "png/014-sonrisa.png",
            ":3": "png/066-perro-6.png"
        }

    def analizador_lexicografico(self):
        texto = self.ui.TXTpWD.toPlainText()
        palabras = self.no_contar_en_ambos(texto)
        emoticones = self.extraer_emoticones(texto)
        emoticones_reemplazados = self.reemplazar_emoticones(texto)

        # Mostrar las palabras y emoticones en el QLabel
        self.ui.lblSalidaRespuesta.setText(f"{emoticones_reemplazados}")
        # Se imprime el contador de palabras y emoticones
        self.ui.lblContador.setText(f"Palabras: {len(palabras)} Emoticones: {len(emoticones)}")


    def extraer_palabras(self, texto):
        # Expresión regular para extraer palabras en español (puedes ajustar según tus necesidades)
        patron_palabras = re.compile(r'\b[\wáéíóúñ]+\b', re.IGNORECASE)
        return patron_palabras.findall(texto)

    def no_contar_en_ambos(self, texto):
        # Esta función se encarga de que si se cuenta en emoticones no se cuente en palabras
        patron_palabras = re.compile(r'\b[^\d\sáéíóúñ]+\b', re.IGNORECASE)
        patron_emoticones = re.compile(r'(?::|;|=|<|x)(?:-)?(?:\)|\(|D|P|O|3|D)|[;:][oO\-]?[D\)\]\(\]/\\OpP]', re.IGNORECASE)
        palabras = patron_palabras.findall(texto)
        emoticones = patron_emoticones.findall(texto)
        for i in range(len(emoticones)):
            for j in range(len(palabras)):
                if emoticones[i] == palabras[j]:
                    del palabras[j]
                    break
        return palabras


    def extraer_emoticones(self, texto):
        # Expresión regular para extraer emoticones (puedes ajustar según tus necesidades)
        patron_emoticones = re.compile(r'(?::|;|=|<|x)(?:-)?(?:\)|\(|D|P|O|3|D)|[;:][oO\-]?[D\)\]\(\]/\\OpP]', re.IGNORECASE)
        return patron_emoticones.findall(texto)

    def reemplazar_emoticones(self, texto):
        # Utilizar una expresión regular para encontrar y reemplazar emoticones
        emoticon_pattern = re.compile('|'.join(re.escape(emoticon) for emoticon in self.diccionario_reemplazo.keys()))

        # Función de reemplazo que utiliza el diccionario de emoticones
        def reemplazo_emoticones(match):
            return f'<img src="{self.diccionario_reemplazo[match.group(0)]}" alt="{match.group(0)}" height="45" width="45">'

        # Realizar el reemplazo en el texto
        texto_con_imagenes = emoticon_pattern.sub(reemplazo_emoticones, texto)

        return texto_con_imagenes


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())

