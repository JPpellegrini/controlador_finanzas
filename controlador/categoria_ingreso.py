import sys
sys.path.append("..")
from vista.tipo_categoria import VentanaCategoriaIngreso
from modelo.modelo import ServiceCategoriaIngreso, CategoriaDTO, NombreError


class ControladorCategoriaIngreso:
    def __init__(self, parent):
        self.__modelo = ServiceCategoriaIngreso()
        self.__vista = VentanaCategoriaIngreso(parent)
        self.__vista.registrar.connect(self.__on_registrar) 

    def __on_registrar(self):
        categoria = self.__vista.obtener_datos()
        try:
            self.__modelo.registrar_cat_ingreso(CategoriaDTO(categoria.nombre, categoria.descripcion))
            self.__vista.verificar_error()
        except NombreError as error:
            self.__vista.verificar_error(error)
    
    def show_vista(self):
        self.__vista.show()
    
    
if __name__ == "__main__":
    from PyQt5 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorCategoriaIngreso()
    controlador.show_vista()
    app.exec()