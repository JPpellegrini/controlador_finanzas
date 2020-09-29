from vista.tipo_categoria import VentanaTipo
from modelo.tipo_transaccion import (
    ServiceTipoTransaccion,
    TipoTransaccionDTO,
    NombreError,
)


class ControladorTipoTransaccion:
    def __init__(self, parent):
        self.__modelo = ServiceTipoTransaccion()
        self.__vista = VentanaTipo(parent)
        self.__vista.registrar.connect(self.__on_registrar)

    def __on_registrar(self):
        tipo = self.__vista.obtener_tipo_transaccion()
        try:
            self.__modelo.registrar_tipo(
                TipoTransaccionDTO(tipo.nombre, tipo.descripcion)
            )
            self.__vista.close()
        except NombreError as error:
            self.__vista.mostrar_error(error)

    def show_vista(self):
        self.__vista.show()
