import sys
sys.path.append("..")
from vista.principal import Vista
from controlador.categoria_egreso import ControladorCategoriaEgreso
from controlador.categoria_ingreso import ControladorCategoriaIngreso
from controlador.egreso import ControladorEgreso
from controlador.ingreso import ControladorIngreso
from controlador.tipo_transaccion import ControladorTipoTransaccion
from modelo.modelo import Balance, Database

class Controlador:
    def __init__(self, db_username, db_password):
        self.__database = Database(db_username, db_password)
        self.__vista = Vista()
        self.__calcular_balance()
        self.__ctl_ingreso = ControladorIngreso(self.__database)
        self.__ctl_egreso = ControladorEgreso(self.__database)
        self.__ctl_tipo = ControladorTipoTransaccion(self.__database)
        self.__ctl_cat_ingreso = ControladorCategoriaIngreso(self.__database)
        self.__ctl_cat_egreso = ControladorCategoriaEgreso(self.__database)

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
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication(sys.argv)
    controlador = Controlador()
    controlador.show_vista()
    app.exec()