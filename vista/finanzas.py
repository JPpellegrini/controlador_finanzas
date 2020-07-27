import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class Vista(QtWidgets.QWidget):
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.__setupUi()

    def __setupUi(self):
        self.__layout = QtWidgets.QFormLayout()

        self.__label_balance = QtWidgets.QLabel('$0')
        self.__btn_calendario = QtWidgets.QPushButton("Calendario")
        self.__btn_ingreso = QtWidgets.QPushButton("+")
        self.__btn_gasto = QtWidgets.QPushButton("-")
        
        self.__layout.addRow("Balance: ", self.__label_balance)
        self.__layout.addRow(self.__btn_calendario)
        self.__layout.addRow(self.__btn_ingreso)
        self.__layout.addRow(self.__btn_gasto)
        
        self.setLayout(self.__layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    vista = Vista()
    vista.show()
    app.exec()