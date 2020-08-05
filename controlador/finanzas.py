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
        self.__vista.agregar_ingreso.connect(lambda: self.__on_agregar_transaccion("ingresos", self.__vista.ventana_agregar_ingreso.obtener_datos()))
        self.__vista.agregar_egreso.connect(lambda: self.__on_agregar_transaccion("egresos", self.__vista.ventana_agregar_egreso.obtener_datos()))
        self.__vista.agregar_movimiento.connect(self.__on_agregar_movimiento)
        self.__vista.agregar_categoria_ingreso.connect(lambda: self.__on_agregar_categoria("categorias_ingreso"))
        self.__vista.agregar_categoria_egreso.connect(lambda: self.__on_agregar_categoria("categorias_egreso"))
        self.__vista.actualizar_mov_cat_ingreso.connect(lambda: self.__vista.ventana_agregar_ingreso.configurar_menu_desplegable(
                                                                self.__obtener_categorias_movimientos("movimientos"),
                                                                self.__obtener_categorias_movimientos("categorias_ingreso"))
                                                                )
        self.__vista.actualizar_mov_cat_egreso.connect(lambda: self.__vista.ventana_agregar_egreso.configurar_menu_desplegable(
                                                                self.__obtener_categorias_movimientos("movimientos"),
                                                                self.__obtener_categorias_movimientos("categorias_egreso"))
                                                                )

    def __obtener_categorias_movimientos(self, tipo):
        diccionario = {}
        for elemento in self.__modelo.buscar(tipo):
            diccionario[elemento[0]] = elemento[1]
        return diccionario

    def __on_calcular_balance(self):
        self.__vista.actualizar_balance(self.__modelo.calcular_balance())

    def __on_agregar_transaccion(self, tipo, datos):
        movimientos = self.__obtener_categorias_movimientos("movimientos")
        if tipo == "ingresos":
            categorias = self.__obtener_categorias_movimientos("categorias_ingreso")
        else:
            categorias = self.__obtener_categorias_movimientos("categorias_egreso")
        
        id_movimiento = list(movimientos.keys())[datos[1]]
        id_categorias = list(categorias.keys())[datos[2]]

        self.__modelo.registrar_transaccion(tipo, TransaccionDTO(datos[0],id_movimiento,id_categorias,datos[3],datos[4],))

    def __on_agregar_movimiento(self):
        datos = self.__vista.ventana_agregar_movimiento.obtener_datos()
        self.__modelo.registrar_movimiento(MovimientoDTO(datos[0], datos[1]))
    
    def __on_agregar_categoria(self, tipo):
        if tipo == "categorias_ingreso": 
            datos = self.__vista.ventana_agregar_categoria_ingreso.obtener_datos()
        else:
            datos = self.__vista.ventana_agregar_categoria_egreso.obtener_datos()
        self.__modelo.registrar_categoria(tipo, CategoriaDTO(datos[0], datos[1]))

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
