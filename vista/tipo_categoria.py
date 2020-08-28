import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class VentanaTipoCategoria(QtWidgets.QDialog):
    registrar = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__setup_ui()
    
    def __setup_ui(self):
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

class VentanaTipo(VentanaTipoCategoria):
    def __init__(self, parent = None):
        VentanaTipoCategoria.__init__(self)
        self.setWindowTitle("Tipo de transaccion")

class VentanaCategoriaIngreso(VentanaTipoCategoria):
    def __init__(self, parent = None):
        VentanaTipoCategoria.__init__(self)
        self.setWindowTitle("Categoria Ingreso")

class VentanaCategoriaEgreso(VentanaTipoCategoria):
    def __init__(self, parent = None):
        VentanaTipoCategoria.__init__(self)
        self.setWindowTitle("Categoria Egreso")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaCategoriaEgreso()
    def visualizar_datos():
        print(ventana.obtener_datos())
    ventana.show()
    ventana.registrar.connect(lambda: visualizar_datos())
    app.exec()