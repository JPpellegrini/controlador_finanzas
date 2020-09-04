import sys
sys.path.append("..")
from vista.tipo_categoria import VentanaCategoriaEgreso
from modelo.modelo import ServiceCategoriaEgreso, CategoriaDTO, NombreError


class ControladorCategoriaEgreso:
    def __init__(self, parent):
        self.__modelo = ServiceCategoriaEgreso()
        self.__vista = VentanaCategoriaEgreso(parent)
        self.__vista.registrar.connect(self.__on_registrar) 

    def __on_registrar(self):
        categoria = self.__vista.obtener_datos()
        try:
            self.__modelo.registrar_cat_egreso(CategoriaDTO(categoria.nombre, categoria.descripcion))
            self.__vista.verificar_error()
        except NombreError as error:
            self.__vista.verificar_error(error)
    
    def show_vista(self):
        self.__vista.show()
    

if __name__ == "__main__":
    from PyQt5 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorCategoriaEgreso()
    controlador.show_vista()
    app.exec()