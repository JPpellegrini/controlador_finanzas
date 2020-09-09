import sys

sys.path.append("..")
from PyQt5 import QtCore, QtWidgets, QtGui
from ui.principal import Ui_VistaPrincipal


class ModeloTablaTransaccion(QtCore.QAbstractTableModel):
    def __init__(self, headers, maps, data):
        super().__init__()
        self.__headers = headers
        self.__column_field_map = maps
        self.__data = data

    def data(self, index: QtCore.QModelIndex, role):
        if role == QtCore.Qt.DisplayRole:
            row_data = self.__data[index.row()]
            column_key = self.__column_field_map[index.column()]
            return row_data[column_key]

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

    def _on_boton_agregar_ingreso(self):
        self.agregar_ingreso.emit()

    def _on_boton_agregar_egreso(self):
        self.agregar_egreso.emit()

    def _on_boton_agregar_tipo_transaccion(self):
        self.agregar_tipo_transaccion.emit()

    def _on_boton_agregar_categoria_ingreso(self):
        self.agregar_categoria_ingreso.emit()

    def _on_boton_agregar_categoria_egreso(self):
        self.agregar_categoria_egreso.emit()

    def actualizar_balance(self, valor):
        self.__ui._line_balance.setText(f"Balance: ${valor}")

    def actualizar_tabla(self, headers: list, maps: dict, data: list):
        self.__modelo = ModeloTablaTransaccion(headers, maps, data)
        self.__ui._table_transaccion.setModel(self.__modelo)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    headers = ["Nombre", "Apellido"]
    maps = {0: "nombre", 1: "apellido"}
    data = [
        dict(nombre="Juan Pablo", apellido="Pellegrini"),
        dict(nombre="Pablo", apellido="Ingegnieri"),
    ]
    ventana = VistaPrincipal()
    ventana.actualizar_balance(1000)
    ventana.actualizar_tabla(headers, maps, data)
    ventana.show()
    app.exec()
