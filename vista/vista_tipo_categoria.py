import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class Ventana_tipo_categoria(QtWidgets.QDialog):
    registrar = QtCore.pyqtSignal()

    def __init__(self, titulo, parent = None):
        QtWidgets.QDialog.__init__(self, parent)

        #CONFIG
        self.setWindowTitle(titulo)

        self.__setupUi()
    
    def __setupUi(self):
        self.__contenedor = QtWidgets.QVBoxLayout()

        #WIDGETS
        self.__line_nombre = QtWidgets.QLineEdit()
        self.__line_descripcion = QtWidgets.QTextEdit()
        self.__label_error = QtWidgets.QLabel("Campos con * obligatorios")
        self.__btn_registrar = QtWidgets.QPushButton("Aceptar")

        self.__line_nombre.setPlaceholderText("Nombre*")
        self.__line_descripcion.setPlaceholderText("Descripción")
        self.__label_error.setStyleSheet("color: gray")
        
        self.__contenedor.addWidget(self.__line_nombre)
        self.__contenedor.addWidget(self.__line_descripcion)
        self.__contenedor.addWidget(self.__label_error)
        self.__contenedor.addWidget(self.__btn_registrar)

        self.__btn_registrar.clicked.connect(self.__on_btn_registrar)

        self.setLayout(self.__contenedor)

    def __on_btn_registrar(self):
        self.registrar.emit()
    
    def __limpiar(self):
        self.__line_nombre.clear()
        self.__line_descripcion.clear()
        self.__label_error.setStyleSheet("color: gray")
        self.__label_error.setText("Campos con * obligatorios")
    
    def verificar_error(self, mensaje_error):
        if mensaje_error != None:
            self.__label_error.setStyleSheet("color: red")
            self.__label_error.setText(mensaje_error)
        else:
            self.__limpiar()
            self.close()

    def closeEvent(self, evnt):
        self.__limpiar()

    def obtener_datos(self):
        return self.__line_nombre.text(), self.__line_descripcion.toPlainText()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana_tipo_categoria("ventana")
    def visualizar_datos():
        print(ventana.obtener_datos())
    ventana.show()
    ventana.registrar.connect(lambda: visualizar_datos())
    app.exec()