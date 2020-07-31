import sys
from PyQt5 import QtWidgets
sys.path.append("..")
from modelo.finanzas import *
from vista.finanzas import *

class Controlador:
    def set_model(self, modelo: Service):
        self.__modelo = modelo

    def set_view(self, vista: Vista):
        self.__vista = vista
        self.__vista.calcular_balance.connect(self.__on_calcular_balance)
        self.__vista.calcular_balance.emit()
        self.__vista.agregar_ingreso.connect(lambda: self.__on_agregar("ingresos"))
        self.__vista.agregar_egreso.connect(lambda: self.__on_agregar("egresos"))
        self.__vista.agregar_movimiento.connect(self.__on_agregar_movimiento)

    def __on_calcular_balance(self):
        self.__vista.actualizar_balance(self.__modelo.calcular_balance())

    def __on_agregar(self, tipo):
        self.__modelo.registrar_transaccion(tipo, TransaccionDTO(self.__vista.obtener_datos(),
                                            1, 1, "hola", "2019"))

    def __on_agregar_movimiento(self):
        datos = self.__vista.ventana_agregar_movimiento.obtener_datos()
        self.__modelo.registrar_movimiento(MovimientoDTO(datos[0], datos[1]))

    def show_vista(self):
        self.__vista.show()
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    modelo = Service()
    vista = Vista()
    controlador = Controlador()

    controlador.set_model(modelo)
    controlador.set_view(vista)
    controlador.show_vista()
    app.exec()
