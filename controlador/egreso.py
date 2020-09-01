import sys
from PyQt5 import QtCore
sys.path.append("..")
from vista.ingreso_egreso import VentanaEgreso
from modelo.modelo import ServiceEgreso, TransaccionDTO, MontoError


class ControladorEgreso(QtCore.QObject):
    actualizar_balance = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__modelo = ServiceEgreso()
        self.__vista = VentanaEgreso()
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        egreso = self.__vista.obtener_datos()
        try:
            self.__modelo.registrar_egreso(TransaccionDTO(egreso.monto, egreso.id_tipo, egreso.id_categoria,\n
                                                            egreso.descripcion, egreso.fecha))
            self.__vista.verificar_error()
            self.actualizar_balance.emit()
        except MontoError as error:
            self.__vista.verificar_error(error)
    
    def show_vista(self):
        tipos_categorias = self.__modelo.obtener_tipos_categorias()
        self.__vista.configurar_menu_desplegable(tipos_categorias[0], tipos_categorias[1])
        self.__vista.show()


if __name__ == "__main__":
    from PyQt5 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorEgreso()
    controlador.show_vista()
    app.exec()