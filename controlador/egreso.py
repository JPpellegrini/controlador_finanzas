import sys
from PyQt5 import QtCore
sys.path.append("..")
from vista.ingreso_egreso import VentanaEgreso, TipoCategoriaDTO
from modelo.modelo import ServiceEgreso, TransaccionDTO, MontoError


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
            self.__modelo.registrar_egreso(TransaccionDTO(egreso.monto, egreso.id_tipo_transaccion, egreso.id_categoria,
                                                            egreso.descripcion, egreso.fecha))
            self.__vista.verificar_error()
            self.actualizar_balance.emit()
        except MontoError as error:
            self.__vista.verificar_error(error)
    
    def show_vista(self):
        tipos_categorias = self.__modelo.obtener_tipos_categorias()
        tipos = [TipoCategoriaDTO(tipo.nombre, tipo.id) for tipo in tipos_categorias["tipos"]]
        categorias = [TipoCategoriaDTO(categoria.nombre, categoria.id) for categoria in tipos_categorias["categorias"]]
        self.__vista.actualizar_tipos_transaccion(tipos)
        self.__vista.actualizar_categorias(categorias)
        self.__vista.show()


if __name__ == "__main__":
    from PyQt5 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorEgreso()
    controlador.show_vista()
    app.exec()