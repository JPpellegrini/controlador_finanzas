import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from vista.vista_tipo_categoria import *
from modelo.modelo import Service_tipo_transaccion as Service, Tipo_transaccionDTO, Database

class Controlador_tipo_transaccion():
    def __init__(self, database):
        self.__modelo = Service(database)
        self.__vista = Ventana_tipo_categoria("Tipo de transaccion")
        self.__vista.registrar.connect(self.__on_registrar_tipo)
    
    def __on_registrar_tipo(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(Tipo_transaccionDTO(datos[0], datos[1])))
    
    def show_vista(self):
        self.__vista.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    base = Database()
    controlador = Controlador_tipo_transaccion(base)
    controlador.show_vista()
    app.exec()



