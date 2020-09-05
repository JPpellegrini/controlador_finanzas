import sys

sys.path.append("..")
from vista.principal import VistaPrincipal
from controlador.categoria_egreso import ControladorCategoriaEgreso
from controlador.categoria_ingreso import ControladorCategoriaIngreso
from controlador.egreso import ControladorEgreso
from controlador.ingreso import ControladorIngreso
from controlador.tipo_transaccion import ControladorTipoTransaccion
from modelo.recursos import Balance


class ControladorPrincipal:
    def __init__(self):
        self.__vista = VistaPrincipal()
        self.__calcular_balance()
        self.__ctl_ingreso = ControladorIngreso(self.__vista)
        self.__ctl_egreso = ControladorEgreso(self.__vista)
        self.__ctl_tipo = ControladorTipoTransaccion(self.__vista)
        self.__ctl_cat_ingreso = ControladorCategoriaIngreso(self.__vista)
        self.__ctl_cat_egreso = ControladorCategoriaEgreso(self.__vista)

        self.__ctl_ingreso.actualizar_balance.connect(self.__on_actualizar_balance)
        self.__ctl_egreso.actualizar_balance.connect(self.__on_actualizar_balance)

        self.__vista.agregar_ingreso.connect(self.__on_agregar_ingreso)
        self.__vista.agregar_egreso.connect(self.__on_agregar_egreso)
        self.__vista.agregar_tipo_transaccion.connect(
            self.__on_agregar_tipo_transaccion
        )
        self.__vista.agregar_categoria_ingreso.connect(
            self.__on_agregar_categoria_ingreso
        )
        self.__vista.agregar_categoria_egreso.connect(
            self.__on_agregar_categoria_egreso
        )

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
        self.__vista.actualizar_balance(Balance.calcular())

    def show_vista(self):
        self.__vista.show()


if __name__ == "__main__":
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorPrincipal()
    controlador.show_vista()
    app.exec()
