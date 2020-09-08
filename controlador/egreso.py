import sys
from PyQt5 import QtCore

sys.path.append("..")
from vista.ingreso_egreso import VentanaEgreso, TipoCategoriaDTO
from modelo.egreso import (
    ServiceEgreso,
    EgresoDTO,
    MontoError,
    TipoError,
    CategoriaError,
)


class ControladorEgreso(QtCore.QObject):
    actualizar_balance = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.__modelo = ServiceEgreso()
        self.__vista = VentanaEgreso(parent)
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        egreso = self.__vista.obtener_transaccion()
        try:
            self.__modelo.registrar_egreso(
                EgresoDTO(
                    egreso.monto,
                    egreso.id_tipo_transaccion,
                    egreso.id_categoria,
                    egreso.descripcion,
                    egreso.fecha,
                )
            )
            self.actualizar_balance.emit()
            self.__vista.close()
        except (MontoError, TipoError, CategoriaError) as error:
            self.__vista.mostrar_error(error)

    def show_vista(self):
        tipos_categorias = self.__modelo.obtener_tipos_categorias()
        self.__vista.actualizar_tipos_transaccion(tipos_categorias["tipos"])
        self.__vista.actualizar_categorias(tipos_categorias["categorias"])
        self.__vista.show()
