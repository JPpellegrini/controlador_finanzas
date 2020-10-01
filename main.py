import sys
import os
from PyQt5 import QtWidgets
from controlador.principal import ControladorPrincipal


app = QtWidgets.QApplication(sys.argv)
controlador = ControladorPrincipal()
controlador.show_vista()
app.exec()
