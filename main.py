import sys
from PyQt5 import QtWidgets
from controlador.principal import *

app = QtWidgets.QApplication(sys.argv)
controlador = Controlador()

app.aboutToQuit.connect(controlador.cerrar_database)
controlador.show_vista()
app.exec()