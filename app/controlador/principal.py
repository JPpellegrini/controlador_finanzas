from vista.principal import VistaPrincipal, TransaccionDTO
from controlador.categoria_egreso import ControladorCategoriaEgreso
from controlador.categoria_ingreso import ControladorCategoriaIngreso
from controlador.egreso import ControladorEgreso
from controlador.ingreso import ControladorIngreso
from controlador.tipo_transaccion import ControladorTipoTransaccion
from modelo.recursos import Balance
from modelo.ingreso import ServiceIngreso, FiltroDTO as FiltroIngresoDTO
from modelo.egreso import ServiceEgreso, FiltroDTO as FiltroEgresoDTO


class ControladorPrincipal:
    def __init__(self):
        self.__modelo_ingreso = ServiceIngreso()
        self.__modelo_egreso = ServiceEgreso()
        self.__vista = VistaPrincipal()
        self.__vista.actualizar_tabla(self.__obtener_transacciones())
        self.__calcular_balance()

        self.__ctl_ingreso = ControladorIngreso(self.__vista)
        self.__ctl_egreso = ControladorEgreso(self.__vista)
        self.__ctl_tipo = ControladorTipoTransaccion(self.__vista)
        self.__ctl_cat_ingreso = ControladorCategoriaIngreso(self.__vista)
        self.__ctl_cat_egreso = ControladorCategoriaEgreso(self.__vista)

        self.__ctl_ingreso.actualizar_balance.connect(self.__on_actualizar_balance)
        self.__ctl_egreso.actualizar_balance.connect(self.__on_actualizar_balance)

        self.__vista.agregar_ingreso.connect(self.__on_agregar_ingreso)
        self.__vista.agregar_egreso.connect(self.__on_agregar_egreso)
        self.__vista.agregar_tipo_transaccion.connect(
            self.__on_agregar_tipo_transaccion
        )
        self.__vista.agregar_categoria_ingreso.connect(
            self.__on_agregar_categoria_ingreso
        )
        self.__vista.agregar_categoria_egreso.connect(
            self.__on_agregar_categoria_egreso
        )
        self.__vista.actualizar_transacciones.connect(self.__on_actualizar_transacciones)

    def __on_agregar_ingreso(self):
        self.__ctl_ingreso.show_vista()

    def __on_agregar_egreso(self):
        self.__ctl_egreso.show_vista()

    def __on_agregar_tipo_transaccion(self):
        self.__ctl_tipo.show_vista()

    def __on_agregar_categoria_ingreso(self):
        self.__ctl_cat_ingreso.show_vista()

    def __on_agregar_categoria_egreso(self):
        self.__ctl_cat_egreso.show_vista()

    def __on_actualizar_balance(self):
        self.__calcular_balance()
        self.__on_actualizar_transacciones()

    def __calcular_balance(self):
        self.__vista.actualizar_balance(Balance.calcular())
    
    def __on_actualizar_transacciones(self):
        fecha = self.__vista.obtener_fecha()
        self.__vista.actualizar_tabla(self.__obtener_transacciones(fecha))

    def __obtener_transacciones(self, fecha=None):
        if fecha:
            lista_ingresos = self.__modelo_ingreso.obtener_ingresos(FiltroIngresoDTO(fecha))
            lista_egresos = self.__modelo_egreso.obtener_egresos(FiltroEgresoDTO(fecha))
        else:
            lista_ingresos = self.__modelo_ingreso.obtener_ingresos()
            lista_egresos = self.__modelo_egreso.obtener_egresos()

        ingresos = [
            TransaccionDTO(
                "ingreso",
                ingreso.monto,
                ingreso.id_tipo_transaccion,
                ingreso.id_categoria,
                ingreso.descripcion,
                ingreso.fecha,
                ingreso.id,
            )
            for ingreso in lista_ingresos
        ]
        egresos = [
            TransaccionDTO(
                "egreso",
                egreso.monto,
                egreso.id_tipo_transaccion,
                egreso.id_categoria,
                egreso.descripcion,
                egreso.fecha,
                egreso.id,
            )
            for egreso in lista_egresos
        ]
        return sorted(ingresos + egresos, key=lambda transaccion: transaccion.fecha, reverse=True)

    def show_vista(self):
        self.__vista.show()
