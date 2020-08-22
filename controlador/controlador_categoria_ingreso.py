import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from vista.vista_tipo_categoria import *
from modelo.modelo import Service_categoria_ingreso as Service, CategoriaDTO

class Controlador_categoria_ingreso:
    def __init__(self, database):
        self.__modelo = Service(database)
        self.__vista = Ventana_tipo_categoria("Categoria de Ingreso")
        self.__vista.registrar.connect(self.__on_agregar_categoria_ingreso) 

    def __on_agregar_categoria_ingreso(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(CategoriaDTO(datos[0], datos[1])))
    
    def show_vista(self):
        self.__vista.show()
    
if __name__ == "__main__":
    from modelo.modelo import Database
    BDD = Database()
    app = QtWidgets.QApplication(sys.argv)
    controlador = Controlador_categoria_ingreso(BDD)

    controlador.show_vista()
    app.exec()