import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from dataclasses import dataclass


@dataclass
class TipoCategoriaDTO:
    nombre: str
    descripcion: str


class VentanaTipoCategoria(QtWidgets.QDialog):
    registrar = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__setup_ui()

    def __setup_ui(self):
        self.__contenedor = QtWidgets.QVBoxLayout()
        self.setWindowModality(QtCore.Qt.WindowModal)

        # WIDGETS
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

    def __set_label_error(self, color, mensaje):
        self.__label_error.setStyleSheet(f"color: {color}")
        self.__label_error.setText(mensaje)

    def __limpiar(self):
        self.__line_nombre.clear()
        self.__line_descripcion.clear()
        self.__set_label_error("gray", "Campos con * obligatorios")

    def closeEvent(self, evnt):
        self.__limpiar()

    def mostrar_error(self, error=None):
        self.__set_label_error("red", str(error))

    def obtener_datos(self):
        nombre = self.__line_nombre.text()
        descripcion = self.__line_descripcion.toPlainText()
        return TipoCategoriaDTO(nombre, descripcion)


class VentanaTipo(VentanaTipoCategoria):
    def __init__(self, parent=None):
        VentanaTipoCategoria.__init__(self, parent)
        self.setWindowTitle("Tipo de transaccion")

    def obtener_tipo_transaccion(self):
        return self.obtener_datos()


class VentanaCategoriaIngreso(VentanaTipoCategoria):
    def __init__(self, parent=None):
        VentanaTipoCategoria.__init__(self, parent)
        self.setWindowTitle("Categoria Ingreso")

    def obtener_cat_ingreso(self):
        return self.obtener_datos()


class VentanaCategoriaEgreso(VentanaTipoCategoria):
    def __init__(self, parent=None):
        VentanaTipoCategoria.__init__(self, parent)
        self.setWindowTitle("Categoria Egreso")

    def obtener_cat_egreso(self):
        return self.obtener_datos()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaCategoriaEgreso()

    def visualizar_datos():
        print(ventana.obtener_datos())

    ventana.show()
    ventana.registrar.connect(lambda: visualizar_datos())
    app.exec()
