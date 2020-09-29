from vista.tipo_categoria import VentanaCategoriaIngreso
from modelo.categoria_ingreso import (
    ServiceCategoriaIngreso,
    CategoriaIngresoDTO,
    NombreError,
)


class ControladorCategoriaIngreso:
    def __init__(self, parent):
        self.__modelo = ServiceCategoriaIngreso()
        self.__vista = VentanaCategoriaIngreso(parent)
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        categoria = self.__vista.obtener_cat_ingreso()
        try:
            self.__modelo.registrar_cat_ingreso(
                CategoriaIngresoDTO(categoria.nombre, categoria.descripcion)
            )
            self.__vista.close()
        except NombreError as error:
            self.__vista.mostrar_error(error)

    def show_vista(self):
        self.__vista.show()
