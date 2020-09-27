import sys

sys.path.append("..")
from PyQt5 import QtCore, QtWidgets, QtGui
from ui.principal import Ui_VistaPrincipal
from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class TransaccionDTO:
    clasificacion: str
    monto: float
    tipo_transaccion: str
    categoria: str
    descripcion: str
    fecha: datetime
    id: int


class ModeloTablaTransaccion(QtCore.QAbstractTableModel):
    def __init__(self, data: list):
        super().__init__()
        self.__headers = ("Monto", "Tipo", "Categoria", "Descripcion", "Fecha")
        self.__data = data

    def get_cell_data(self, data_row: object, index: int):
        column_field_map = {
            0: "$ " + str(data_row.monto),
            1: data_row.tipo_transaccion,
            2: data_row.categoria,
            3: data_row.descripcion,
            4: data_row.fecha.strftime("%d/%m/%Y"),
        }
        return column_field_map[index]

    def data(self, index: QtCore.QModelIndex, role):
        data_row = self.__data[index.row()]

        if role == QtCore.Qt.DisplayRole:
            data_cell = self.get_cell_data(data_row, index.column())
            return data_cell

        if role == QtCore.Qt.ForegroundRole:
            if index.column() == 0:
                if data_row.clasificacion == "ingreso":
                    return QtGui.QColor("#11a64f")
                if data_row.clasificacion == "egreso":
                    return QtGui.QColor("#a61111")

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
    actualizar_transacciones = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__ui = Ui_VistaPrincipal()
        self.__setupUi()

    def __setupUi(self):
        self.__ui.setupUi(self)
        self.__selected_date = None

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

    def on_click_calendario(self):
        self.actualizar_transacciones.emit()

    def actualizar_tabla(self, data: list):
        self.__transacciones = data
        self.__modelo = ModeloTablaTransaccion(self.__transacciones)
        self.__ui.table_transaccion.setModel(self.__modelo)

    def actualizar_balance(self, valor: float):
        self.__ui.line_balance.setText(f"Balance: ${valor}")

    def obtener_fecha(self):
        self.__selected_date = self.__ui.calendario.selectedDate()
        return self.__selected_date.toPyDate()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ventana = VistaPrincipal()
    ventana.actualizar_balance(1000)
    ventana.show()
    app.exec()
