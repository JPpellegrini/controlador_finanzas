import sys

sys.path.append("..")
from PyQt5 import QtCore, QtWidgets, QtGui
from ui.principal import Ui_VistaPrincipal
from dataclasses import dataclass


@dataclass
class TransaccionDTO:
    clasificacion: str
    monto: str
    tipo_transaccion: str
    categoria: str
    descripcion: str
    fecha: str
    id: int


class ModeloTablaTransaccion(QtCore.QAbstractTableModel):
    def __init__(self, data: list):
        super().__init__()
        self.__headers = ("Monto", "Tipo", "Categoria", "Descripcion")
        self.__data = data

    def get_cell_data(self, data_row: object, index: int):
        column_field_map = {
            0: data_row.monto,
            1: data_row.tipo_transaccion,
            2: data_row.categoria,
            3: data_row.descripcion,
        }
        return column_field_map[index]

    def data(self, index: QtCore.QModelIndex, role):
        data_row = self.__data[index.row()]

        if role == QtCore.Qt.DisplayRole:
            data_cell = self.get_cell_data(data_row, index.column())
            return data_cell

        if role == QtCore.Qt.BackgroundRole:
            if data_row.clasificacion == "ingreso":
                return QtGui.QColor("#aeebab")
            if data_row.clasificacion == "egreso":
                return QtGui.QColor("#f0c5c2")

    def rowCount(self, index):
        return len(self.__data)

    def columnCount(self, parent):
        return len(self.__headers)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.__headers[section]


class VistaPrincipal(QtWidgets.QMainWindow):

    agregar_ingreso = QtCore.pyqtSignal()
    agregar_egreso = QtCore.pyqtSignal()
    agregar_tipo_transaccion = QtCore.pyqtSignal()
    agregar_categoria_ingreso = QtCore.pyqtSignal()
    agregar_categoria_egreso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__ui = Ui_VistaPrincipal()
        self.__setupUi()

    def __setupUi(self):
        self.__ui.setupUi(self)
        self.__selected_date = False

    def on_boton_agregar_ingreso(self):
        self.agregar_ingreso.emit()

    def on_boton_agregar_egreso(self):
        self.agregar_egreso.emit()

    def on_boton_agregar_tipo_transaccion(self):
        self.agregar_tipo_transaccion.emit()

    def on_boton_agregar_categoria_ingreso(self):
        self.agregar_categoria_ingreso.emit()

    def on_boton_agregar_categoria_egreso(self):
        self.agregar_categoria_egreso.emit()

    def __actualizar_tabla(self, selected_date: bool):
        data = self.__transacciones
        if selected_date:
            fecha = self.__ui.calendario.selectedDate()
            data = [
                transaccion
                for transaccion in self.__transacciones
                if transaccion.fecha == fecha.toPyDate()
            ]
        self.__modelo = ModeloTablaTransaccion(data)
        self.__table_transaccion.setModel(self.__modelo)

    def actualizar_transacciones(self, transacciones: list):
        self.__transacciones = transacciones
        self.__actualizar_tabla(self.__selected_date)
        if not self.__selected_date:
            self.__selected_date = True

    def actualizar_balance(self, valor: float):
        self.__ui.line_balance.setText(f"Balance: ${valor}")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ventana = VistaPrincipal()
    ventana.actualizar_balance(1000)
    ventana.show()
    app.exec()
