import sys
sys.path.append("..")
from vista.vista_ingreso_egreso import *
from modelo.modelo import Service_egreso as Service, TransaccionDTO,\
    Database, Service_tipo_transaccion as Tipos, Service_categoria_egreso as Categorias


class Controlador_egreso(QtCore.QObject):
    actualizar_balance = QtCore.pyqtSignal()

    def __init__(self, database):
        super().__init__()
        self.__modelo = Service(database)
        self.__vista = Ventana_ingreso_egreso("Egreso")
        self.__vista.registrar.connect(self.__on_registrar_egreso)

    def __on_registrar_egreso(self):
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
    app = QtWidgets.QApplication(sys.argv)
    base = Database()
    controlador = Controlador_ingreso(base)
    controlador.show_vista()
    app.exec()