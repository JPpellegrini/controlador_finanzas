import sys
from PyQt5 import QtCore, QtWidgets, QtGui

class Vista(QtWidgets.QWidget):
    
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.__setupUi()

    def __setupUi(self):
        self.__layout = QtWidgets.QFormLayout()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    vista = Vista()
    vista.show()
    app.exec()