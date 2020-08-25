import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from vista.vista_principal import *
from controlador.controlador_categoria_egreso import *
from controlador.controlador_categoria_ingreso import *
from controlador.controlador_egreso import *
from controlador.controlador_ingreso import *
from controlador.controlador_tipo_transaccion import *
from modelo.modelo import Balance, Database

class Controlador:
    def __init__(self):
        self.__database = Database()
        self.__vista = Vista()
        self.__calcular_balance()
        self.__ctl_ingreso = Controlador_ingreso(self.__database)
        self.__ctl_egreso = Controlador_egreso(self.__database)
        self.__ctl_tipo = Controlador_tipo_transaccion(self.__database)
        self.__ctl_cat_ingreso = Controlador_categoria_ingreso(self.__database)
        self.__ctl_cat_egreso = Controlador_categoria_egreso(self.__database)

        self.__ctl_ingreso.actualizar_balance.connect(self.__on_actualizar_balance)
        self.__ctl_egreso.actualizar_balance.connect(self.__on_actualizar_balance)

        self.__vista.agregar_ingreso.connect(self.__on_agregar_ingreso)
        self.__vista.agregar_egreso.connect(self.__on_agregar_egreso)
        self.__vista.agregar_tipo_transaccion.connect(self.__on_agregar_tipo_transaccion)
        self.__vista.agregar_categoria_ingreso.connect(self.__on_agregar_categoria_ingreso)
        self.__vista.agregar_categoria_egreso.connect(self.__on_agregar_categoria_egreso)


    def __on_agregar_ingreso(self):
        self.__ctl_ingreso.show_vista()

    def __on_agregar_egreso(self):
        self.__ctl_egreso.show_vista()
    
    def __on_agregar_tipo_transaccion(self):
        self.__ctl_tipo.show_vista()
    
    def __on_agregar_categoria_ingreso(self):
        self.__ctl_cat_ingreso.show_vista()

    def __on_agregar_categoria_egreso(self):
        self.__ctl_cat_egreso.show_vista()

    def __on_actualizar_balance(self):
        self.__calcular_balance()

    def __calcular_balance(self):
        self.__vista.actualizar_balance(Balance.calcular(self.__database))

    def show_vista(self):
        self.__vista.show()
    
    def cerrar_database(self):
        self.__database.cerrar()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controlador = Controlador()
    controlador.show_vista()
    app.exec()