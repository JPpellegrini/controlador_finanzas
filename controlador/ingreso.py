import sys
from PyQt5 import QtCore
sys.path.append("..")
from vista.ingreso_egreso import VentanaIngreso, TipoCategoriaDTO
from modelo.modelo import ServiceIngreso, TransaccionDTO, MontoError, TipoError, CategoriaError


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
            self.__modelo.registrar_ingreso(TransaccionDTO(ingreso.monto, ingreso.id_tipo_transaccion, ingreso.id_categoria,
                                                            ingreso.descripcion, ingreso.fecha))
            self.actualizar_balance.emit()
            self.__vista.close()
        except Exception as error:
            self.__vista.mostrar_error(error)
    
    def show_vista(self):
        tipos_categorias = self.__modelo.obtener_tipos_categorias()
        self.__vista.enviar_datos(tipos_categorias["tipos"], tipos_categorias["categorias"])
        self.__vista.show()
   

if __name__ == "__main__":
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorIngreso()
    controlador.show_vista()
    app.exec()