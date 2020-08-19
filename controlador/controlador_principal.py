import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from vista.vista_principal import *

class Controlador:

    def set_view(self, vista: Vista):
        self.__vista = vista
        self.__vista.calcular_balance.connect(self.__on_calcular_balance)
        self.__vista.calcular_balance.emit()

    def __on_calcular_balance(self):
        self.__vista.actualizar_balance(1000)

    def show_vista(self):
        self.__vista.show()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    vista = Vista()
    controlador = Controlador()

    controlador.set_view(vista)
    controlador.show_vista()
    app.exec()