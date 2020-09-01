import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class ModeloTablaTransaccion(QtCore.QAbstractTableModel):
    def __init__(self,headers, maps, data):
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


class VistaPrincipal(QtWidgets.QWidget):
    
    #SIGNALS
    agregar_ingreso = QtCore.pyqtSignal()
    agregar_egreso = QtCore.pyqtSignal()
    agregar_tipo_transaccion = QtCore.pyqtSignal()
    agregar_categoria_ingreso = QtCore.pyqtSignal()
    agregar_categoria_egreso = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.__setup_ui()

    def __setup_ui(self):
        self.setWindowTitle("Controlador de Finanzas")
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__btn_layout = QtWidgets.QVBoxLayout()
        self.__cal_layout = QtWidgets.QVBoxLayout()
        self.__opcion_layout = QtWidgets.QHBoxLayout()

        #WIDGETS
        self.__line_balance = QtWidgets.QLineEdit()
        self.__btn_ingreso = QtWidgets.QPushButton("Nuevo Ingreso")
        self.__btn_egreso = QtWidgets.QPushButton("Nuevo Egreso")
        self.__btn_tipo_transaccion = QtWidgets.QPushButton("Nuevo Tipo de Transaccion")
        self.__btn_categoria_ingreso = QtWidgets.QPushButton("Nueva Categoria de Ingreso")
        self.__btn_categoria_egreso = QtWidgets.QPushButton("Nueva Categoria de Egreso")
        self.__calendario = QtWidgets.QCalendarWidget()
        self.__label_transaccion = QtWidgets.QLabel('Transacciones')
        self.__table_transaccion = QtWidgets.QTableView()
        self.__btn_editar = QtWidgets.QPushButton("Editar")
        self.__btn_eliminar = QtWidgets.QPushButton("Eliminar")
        self.__spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        #CONFIG WIDGETS
        self.__line_balance.setReadOnly(True)
        self.__btn_editar.setEnabled(False)
        self.__btn_eliminar.setEnabled(False)
        self.__label_transaccion.setStyleSheet("color: #1E90FF")

        #IPLEMENTACION WIDGETS        
        self.__btn_layout.addWidget(self.__btn_ingreso)
        self.__btn_layout.addWidget(self.__btn_egreso)
        self.__btn_layout.addWidget(self.__btn_tipo_transaccion)
        self.__btn_layout.addWidget(self.__btn_categoria_ingreso)
        self.__btn_layout.addWidget(self.__btn_categoria_egreso)
        self.__btn_layout.addSpacerItem(self.__spacer)
        self.__btn_layout.addWidget(self.__line_balance)
        self.__cal_layout.addWidget(self.__calendario)
        self.__cal_layout.addWidget(self.__label_transaccion)
        self.__cal_layout.addWidget(self.__table_transaccion)
        self.__opcion_layout.addWidget(self.__btn_editar)
        self.__opcion_layout.addWidget(self.__btn_eliminar)

        #BOTONES
        self.__btn_ingreso.clicked.connect(lambda: self.agregar_ingreso.emit())
        self.__btn_egreso.clicked.connect(lambda: self.agregar_egreso.emit())
        self.__btn_tipo_transaccion.clicked.connect(lambda: self.agregar_tipo_transaccion.emit())
        self.__btn_categoria_ingreso.clicked.connect(lambda: self.agregar_categoria_ingreso.emit())
        self.__btn_categoria_egreso.clicked.connect(lambda: self.agregar_categoria_egreso.emit())
                
        self.__main_layout.addLayout(self.__btn_layout)
        self.__main_layout.addLayout(self.__cal_layout)
        self.__btn_layout.addLayout(self.__opcion_layout)
        self.setLayout(self.__main_layout)

    def actualizar_balance(self, valor):
        self.__line_balance.setText(f"Balance: {valor}")
    
    def setear_tabla(self, headers = list, maps = dict, data = list):
        self.__modelo = ModeloTablaTransaccion(headers, maps, data)
        self.__table_transaccion.setModel(self.__modelo)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    headers=["Nombre","Apellido"]
    maps={0:"nombre",1:"apellido"}
    data=[dict(nombre="Juan Pablo",apellido="Pellegrini"),dict(nombre="Pablo",apellido="Ingegnieri")]
    ventana = VistaPrincipal()
    ventana.actualizar_balance(1000)
    ventana.setear_tabla(headers,maps,data)
    ventana.show()
    app.exec()