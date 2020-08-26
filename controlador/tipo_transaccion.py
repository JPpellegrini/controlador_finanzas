import sys
sys.path.append("..")
from vista.tipo_categoria import VentanaTipo
from modelo.modelo import ServiceTipoTransaccion as Service, TipoTransaccionDTO


class ControladorTipoTransaccion():
    def __init__(self, database):
        self.__modelo = Service(database)
        self.__vista = VentanaTipo()
        self.__vista.registrar.connect(self.__on_registrar)
    
    def __on_registrar(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(TipoTransaccionDTO(datos[0], datos[1])))
    
    def show_vista(self):
        self.__vista.show()


if __name__ == "__main__":
    from modelo.modelo import Database
    from PyQt5 import QtCore, QtWidgets, QtGui

    app = QtWidgets.QApplication(sys.argv)
    base = Database()
    controlador = ControladorTipoTransaccion(base)
    controlador.show_vista()
    app.exec()



