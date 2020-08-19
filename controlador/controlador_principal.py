import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from vista.vista_principal import *

class Controlador:
    def __init__(self):
        self.__vista = Vista()
        self.__vista.calcular_balance.connect(self.__on_calcular_balance)

    def __on_calcular_balance(self):
        self.__vista.actualizar_balance(1000)

    def show_vista(self):
        self.__vista.show()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controlador = Controlador()

    controlador.show_vista()
    app.exec()