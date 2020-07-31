import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class Ventana_movimiento(QtWidgets.QDialog):

    signal = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__setupUi()
    
    def __setupUi(self):
        self.__contenedor = QtWidgets.QVBoxLayout()

        #WIDGETS
        self.__line_nombre = QtWidgets.QLineEdit()
        self.__line_descripcion = QtWidgets.QTextEdit()
        self.__btn_registrar = QtWidgets.QPushButton("Aceptar")
        
        self.__line_nombre.setPlaceholderText("Nombre")
        self.__line_descripcion.setPlaceholderText("Descripción")
        
        self.__contenedor.addWidget(self.__line_nombre)
        self.__contenedor.addWidget(self.__line_descripcion)
        self.__contenedor.addWidget(self.__btn_registrar)

        self.__btn_registrar.clicked.connect(self.__on_btn_registrar)

        self.setLayout(self.__contenedor)

    def __on_btn_registrar(self):
        self.signal.emit()
        self.close()
    
    def obtener_datos(self):
        return self.__line_nombre.text(), self.__line_descripcion.toPlainText()
    

class Vista(QtWidgets.QWidget):
    
    calcular_balance = QtCore.pyqtSignal()
    agregar_ingreso = QtCore.pyqtSignal()
    agregar_egreso = QtCore.pyqtSignal()
    agregar_movimiento = QtCore.pyqtSignal()


    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ventana_movimiento = Ventana_movimiento()
        self.ventana_movimiento.signal.connect(lambda: self.agregar_movimiento.emit())
        self.__setupUi()

    def __setupUi(self):
        self.__layout = QtWidgets.QFormLayout()

        #WIDGETS
        self.__label_balance = QtWidgets.QLabel('$0')
        self.__btn_calendario = QtWidgets.QPushButton("Calendario")
        self.__line_cantidad = QtWidgets.QLineEdit()
        self.__btn_ingreso = QtWidgets.QPushButton("+")
        self.__btn_egreso = QtWidgets.QPushButton("-")
        self.__btn_movimiento = QtWidgets.QPushButton("Agregar movimiento")
        self.__btn_categoria_ingreso = QtWidgets.QPushButton("Agregar categoria de ingreso")
        
        self.__layout.addRow("Balance: ", self.__label_balance)
        self.__layout.addRow(self.__btn_calendario)
        self.__layout.addRow(self.__line_cantidad)
        self.__layout.addRow(self.__btn_ingreso)
        self.__layout.addRow(self.__btn_egreso)
        self.__layout.addRow(self.__btn_movimiento)
        self.__layout.addRow(self.__btn_categoria_ingreso)

        self.__btn_ingreso.clicked.connect(self.__on_btn_ingreso_clicked)
        self.__btn_egreso.clicked.connect(self.__on_btn_egreso_clicked)
        self.__btn_movimiento.clicked.connect(self.__on_btn_movimiento_clicked)
        self.__btn_categoria_ingreso.clicked.connect(self.__on_btn_categoria_ingreso_clicked)
                
        self.setLayout(self.__layout)
    
    def __on_btn_ingreso_clicked(self):
        self.agregar_ingreso.emit()
        self.calcular_balance.emit()

    def __on_btn_egreso_clicked(self):
        self.agregar_egreso.emit()
        self.calcular_balance.emit()

    def __on_btn_movimiento_clicked(self):
        self.ventana_movimiento.exec_()

    def __on_btn_categoria_ingreso_clicked(self):
        pass

    def obtener_datos(self):
        return float(self.__line_cantidad.text())

    def actualizar_balance(self, valor):
        self.__label_balance.setText(str(valor))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    vista = Vista()
    vista.show()
    app.exec()