import sys
sys.path.append("..")
from vista.tipo_categoria import VentanaTipo
from modelo.tipo_transaccion import ServiceTipoTransaccion, TipoTransaccionDTO, NombreError


class ControladorTipoTransaccion():
    def __init__(self, parent):
        self.__modelo = ServiceTipoTransaccion()
        self.__vista = VentanaTipo(parent)
        self.__vista.registrar.connect(self.__on_registrar)
    
    def __on_registrar(self):
        tipo = self.__vista.obtener_datos()
        try:
            self.__modelo.registrar_tipo(TipoTransaccionDTO(tipo.nombre, tipo.descripcion))
            self.__vista.verificar_error()
        except NombreError as error:
            self.__vista.verificar_error(error)
        
    def show_vista(self):
        self.__vista.show()


if __name__ == "__main__":
    from PyQt5 import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    controlador = ControladorTipoTransaccion()
    controlador.show_vista()
    app.exec()



