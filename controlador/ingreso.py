import sys
from PyQt5 import QtCore
sys.path.append("..")
from vista.ingreso_egreso import VentanaIngreso
from modelo.modelo import ServiceIngreso, TransaccionDTO, MontoError


class ControladorIngreso(QtCore.QObject):
    actualizar_balance = QtCore.pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.__modelo = ServiceIngreso()
        self.__vista = VentanaIngreso(parent)
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        ingreso = self.__vista.obtener_datos()
        try:
            self.__modelo.registrar_ingreso(TransaccionDTO(ingreso.monto, ingreso.id_tipo, ingreso.id_categoria,
                                                            ingreso.descripcion, ingreso.fecha))
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
    controlador = ControladorIngreso()
    controlador.show_vista()
    app.exec()