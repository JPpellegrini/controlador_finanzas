import sys

sys.path.append("..")
from PyQt5 import QtCore, QtWidgets, QtGui
from dataclasses import dataclass
from ui.tipo_categoria import Ui_VentanaTipoCategoria


@dataclass
class TipoCategoriaDTO:
    nombre: str
    descripcion: str


class VentanaTipoCategoria(QtWidgets.QWidget):
    registrar = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()
        self.__ui = Ui_VentanaTipoCategoria()
        self.__setupUi()

    def __setupUi(self):
        self.__ui.setupUi(self)

    def _on_button_aceptar(self):
        self.registrar.emit()

    def __set_label_error(self, color, mensaje):
        self.__ui._label_error.setStyleSheet(f"color: {color}")
        self.__ui._label_error.setText(mensaje)

    def __limpiar(self):
        self.__ui._line_nombre.clear()
        self.__ui._text_descripcion.clear()
        self.__ui._label_error.setText("")

    def closeEvent(self, evnt):
        self.__limpiar()

    def mostrar_error(self, error=None):
        self.__set_label_error("red", str(error))

    def obtener_datos(self):
        nombre = self.__ui._line_nombre.text()
        descripcion = self.__ui._text_descripcion.toPlainText()
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
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaTipoCategoria()
    ventana.registrar.connect(lambda: print(ventana.obtener_datos()))
    ventana.show()

    app.exec()
