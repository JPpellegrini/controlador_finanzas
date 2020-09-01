import sys
sys.path.append("..")
from vista.tipo_categoria import VentanaCategoriaIngreso
from modelo.modelo import ServiceCategoriaIngreso as Service, CategoriaDTO


class ControladorCategoriaIngreso:
    def __init__(self, parent):
        self.__modelo = Service()
        self.__vista = VentanaCategoriaIngreso(parent)
        self.__vista.registrar.connect(self.__on_registrar) 

    def __on_registrar(self):
        datos = self.__vista.obtener_datos()
        self.__vista.verificar_error(self.__modelo.registrar(CategoriaDTO(datos[0], datos[1])))
    
    def show_vista(self):
        self.__vista.show()
    
    
if __name__ == "__main__":
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorCategoriaIngreso()
    controlador.show_vista()
    app.exec()