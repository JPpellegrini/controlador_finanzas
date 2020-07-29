import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class Vista(QtWidgets.QWidget):
    
    calcular_balance = QtCore.pyqtSignal()
    agregar_ingreso = QtCore.pyqtSignal()
    agregar_egreso = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.__setupUi()

    def __setupUi(self):
        self.__layout = QtWidgets.QFormLayout()

        #WIDGETS
        self.__label_balance = QtWidgets.QLabel('$0')
        self.__btn_calendario = QtWidgets.QPushButton("Calendario")
        self.__line_cantidad = QtWidgets.QLineEdit()
        self.__btn_ingreso = QtWidgets.QPushButton("+")
        self.__btn_egreso = QtWidgets.QPushButton("-")
        
        self.__layout.addRow("Balance: ", self.__label_balance)
        self.__layout.addRow(self.__btn_calendario)
        self.__layout.addRow(self.__line_cantidad)
        self.__layout.addRow(self.__btn_ingreso)
        self.__layout.addRow(self.__btn_egreso)

        self.__btn_ingreso.clicked.connect(self.__on_btn_ingreso_clicked)
        self.__btn_egreso.clicked.connect(self.__on_btn_egreso_clicked)
                
        self.setLayout(self.__layout)
    
    def __on_btn_ingreso_clicked(self):
        self.agregar_ingreso.emit()
        self.calcular_balance.emit()

    def __on_btn_egreso_clicked(self):
        self.agregar_egreso.emit()
        self.calcular_balance.emit()

    def obtener_datos(self):
        return float(self.__line_cantidad.text())

    def actualizar_balance(self, valor):
        self.__label_balance.setText(str(valor))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    vista = Vista()
    vista.show()
    app.exec()