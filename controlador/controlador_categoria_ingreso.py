import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from vista.vista_tipo_categoria import *
from modelo.modelo import ServiceCategoriaIngreso as Service, CategoriaDTO

class ControladorCategoriaIngreso:
    def __init__(self, database):
        self.__modelo = Service(database)
        self.__vista = VentanaTipoCategoria("Categoria de Ingreso")
        self.__vista.registrar.connect(self.__on_registrar) 

    def __on_registrar(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(CategoriaDTO(datos[0], datos[1])))
    
    def show_vista(self):
        self.__vista.show()
    
if __name__ == "__main__":
    from modelo.modelo import Database
    BDD = Database()
    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorCategoriaIngreso(BDD)

    controlador.show_vista()
    app.exec()