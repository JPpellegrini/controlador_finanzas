from vista.tipo_categoria import VentanaCategoriaEgreso
from modelo.categoria_egreso import (
    ServiceCategoriaEgreso,
    CategoriaEgresoDTO,
    NombreError,
)


class ControladorCategoriaEgreso:
    def __init__(self, parent):
        self.__modelo = ServiceCategoriaEgreso()
        self.__vista = VentanaCategoriaEgreso(parent)
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        categoria = self.__vista.obtener_cat_egreso()
        try:
            self.__modelo.registrar_cat_egreso(
                CategoriaEgresoDTO(categoria.nombre, categoria.descripcion)
            )
            self.__vista.close()
        except NombreError as error:
            self.__vista.mostrar_error(error)

    def show_vista(self):
        self.__vista.show()
