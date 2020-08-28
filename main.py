import sys
import os
from PyQt5 import QtWidgets
from controlador.principal import Controlador
from dotenv import load_dotenv
load_dotenv()

app = QtWidgets.QApplication(sys.argv)
controlador = Controlador()

#app.aboutToQuit.connect()
controlador.show_vista()
app.exec()