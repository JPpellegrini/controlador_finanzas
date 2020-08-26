import sys
from PyQt5 import QtCore
sys.path.append("..")
from vista.ingreso_egreso import VentanaEgreso
from modelo.modelo import ServiceEgreso as Service, TransaccionDTO


class ControladorEgreso(QtCore.QObject):
    actualizar_balance = QtCore.pyqtSignal()

    def __init__(self, database):
        super().__init__()
        self.__modelo = Service(database)
        self.__vista = VentanaEgreso()
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(
            TransaccionDTO(datos[0], datos[1], datos[2], datos[3], datos[4]))
        )
        self.actualizar_balance.emit()
    
    def show_vista(self):
        tipos_categorias = self.__modelo.obtener_tipos_categorias()
        self.__vista.configurar_menu_desplegable(tipos_categorias[0], tipos_categorias[1])
        self.__vista.show()


if __name__ == "__main__":
    from modelo.modelo import Database
    from PyQt5 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    base = Database()
    controlador = ControladorEgreso(base)
    controlador.show_vista()
    app.exec()