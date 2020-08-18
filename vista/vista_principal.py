import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class Vista(QtWidgets.QWidget):
    
    #SIGNALS
    calcular_balance = QtCore.pyqtSignal()
    agregar_ingreso = QtCore.pyqtSignal()
    agregar_egreso = QtCore.pyqtSignal()
    agregar_tipo_transaccion = QtCore.pyqtSignal()
    agregar_categoria_ingreso = QtCore.pyqtSignal()
    agregar_categoria_egreso = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        #CONFIG
        self.setWindowTitle("Controlador de Finanzas")

        self.__setupUi()

    def __setupUi(self):
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
        self.__label_ingresos = QtWidgets.QLabel('Ingresos')
        self.__tree_ingresos = QtWidgets.QTreeView()
        self.__label_egresos = QtWidgets.QLabel('Egresos')
        self.__tree_egresos = QtWidgets.QTreeView()
        self.__btn_editar = QtWidgets.QPushButton("Editar")
        self.__btn_eliminar = QtWidgets.QPushButton("Eliminar")

        #CONFIG WIDGETS
        self.__line_balance.setReadOnly(1)
        self.__btn_editar.setEnabled(False)
        self.__btn_eliminar.setEnabled(False)
        self.__label_ingresos.setStyleSheet("color: green")
        self.__label_egresos.setStyleSheet("color: red")

        #IPLEMENTACION WIDGETS
        self.__main_layout.addLayout(self.__btn_layout)
        self.__main_layout.addLayout(self.__cal_layout)
        
        self.__btn_layout.addWidget(self.__btn_ingreso)
        self.__btn_layout.addWidget(self.__btn_egreso)
        self.__btn_layout.addWidget(self.__btn_tipo_transaccion)
        self.__btn_layout.addWidget(self.__btn_categoria_ingreso)
        self.__btn_layout.addWidget(self.__btn_categoria_egreso)
        self.__btn_layout.addWidget(self.__line_balance)

        self.__cal_layout.addWidget(self.__calendario)
        self.__cal_layout.addWidget(self.__label_ingresos)
        self.__cal_layout.addWidget(self.__tree_ingresos)
        self.__cal_layout.addWidget(self.__label_egresos)
        self.__cal_layout.addWidget(self.__tree_egresos)

        self.__btn_layout.addLayout(self.__opcion_layout)
        self.__opcion_layout.addWidget(self.__btn_editar)
        self.__opcion_layout.addWidget(self.__btn_eliminar)

        #BOTONES
        self.__btn_ingreso.clicked.connect(lambda: self.agregar_ingreso.emit())
        self.__btn_egreso.clicked.connect(lambda: self.agregar_egreso.emit())
        self.__btn_tipo_transaccion.clicked.connect(lambda: self.agregar_tipo_transaccion.emit())
        self.__btn_categoria_ingreso.clicked.connect(lambda: self.agregar_categoria_ingreso.emit())
        self.__btn_categoria_egreso.clicked.connect(lambda: self.agregar_categoria_egreso.emit())
                
        self.setLayout(self.__main_layout)

    def actualizar_balance(self, valor):
        self.__line_balance.setText("Balance: " + str(valor))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Vista()
    ventana.actualizar_balance(1000)
    ventana.show()
    app.exec()