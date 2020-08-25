import sys
sys.path.append("..")
from vista.tipo_categoria import VentanaTipoCategoria
from modelo.modelo import ServiceCategoriaEgreso as Service, CategoriaDTO

class Controlador_categoria_egreso:
    def __init__(self, database):
        self.__modelo = Service(database)
        self.__vista = Ventana_tipo_categoria("Categoria de Egreso")
        self.__vista.registrar.connect(self.__on_agregar_categoria_egreso) 

    def __on_agregar_categoria_egreso(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(CategoriaDTO(datos[0], datos[1])))
    
    def show_vista(self):
        self.__vista.show()
    
if __name__ == "__main__":
    from PyQt5 import QtWidgets
    from modelo.modelo import Database
    BDD = Database()
    app = QtWidgets.QApplication(sys.argv)
    controlador = Controlador_categoria_egreso(BDD)
    controlador.show_vista()
    app.exec()