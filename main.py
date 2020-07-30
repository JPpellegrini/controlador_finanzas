import sys
from PyQt5 import QtWidgets
from modelo.finanzas import *
from vista.finanzas import *
from controlador.finanzas import *

app = QtWidgets.QApplication(sys.argv)
modelo = Service()
vista = Vista()
controlador = Controlador()

controlador.set_model(modelo)
controlador.set_view(vista)
app.aboutToQuit.connect(modelo.cerrar_database)
controlador.show_vista()
app.exec()