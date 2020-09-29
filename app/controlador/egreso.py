from PyQt5 import QtCore

from app.vista.ingreso_egreso import VentanaEgreso, TipoCategoriaDTO
from app.modelo.egreso import (
    ServiceEgreso,
    EgresoDTO,
    MontoError,
    TipoError,
    CategoriaError,
)
from app.modelo.tipo_transaccion import ServiceTipoTransaccion as TipoTransaccion
from app.modelo.categoria_egreso import ServiceCategoriaEgreso as CategoriaEgreso


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

    def __actualizar_tipos_categorias(self):
        self.__vista.actualizar_tipos_transaccion(TipoTransaccion().obtener_tipos())
        self.__vista.actualizar_categorias(CategoriaEgreso().obtener_cat_egreso())

    def show_vista(self):
        self.__actualizar_tipos_categorias()
        self.__vista.show()
