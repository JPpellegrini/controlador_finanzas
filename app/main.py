from PyQt5 import QtWidgets

from app.controlador.principal import ControladorPrincipal


app = QtWidgets.QApplication([])
controlador = ControladorPrincipal()
controlador.show_vista()
app.exec()
