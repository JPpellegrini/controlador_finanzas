import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from dataclasses import dataclass

@dataclass
class TransaccionDTO:
    monto: str
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: str

class VentanaIngresoEgreso(QtWidgets.QDialog):
    registrar = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__setup_ui()
    
    def __setup_ui(self):
        self.__contenedor = QtWidgets.QVBoxLayout()

        #WIDGETS
        self.__line_monto = QtWidgets.QLineEdit()
        self.__cbx_tipo_transaccion = QtWidgets.QComboBox()
        self.__cbx_categorias = QtWidgets.QComboBox()
        self.__line_descripcion = QtWidgets.QTextEdit()
        self.__cal_fecha = QtWidgets.QCalendarWidget()
        self.__label_error = QtWidgets.QLabel("Campos con * obligatorios")
        self.__boton = QtWidgets.QPushButton("Aceptar")
        
        self.__line_monto.setPlaceholderText("Monto*")
        self.__cbx_tipo_transaccion.setPlaceholderText("Tipo de Transaccion*")
        self.__cbx_categorias.setPlaceholderText("Categoria*")
        self.__line_descripcion.setPlaceholderText("Descripcion")
        self.__label_error.setStyleSheet("color: gray")
        
        self.__contenedor.addWidget(self.__line_monto)
        self.__contenedor.addWidget(self.__cbx_tipo_transaccion)
        self.__contenedor.addWidget(self.__cbx_categorias)
        self.__contenedor.addWidget(self.__line_descripcion)
        self.__contenedor.addWidget(self.__cal_fecha)
        self.__contenedor.addWidget(self.__label_error)
        self.__contenedor.addWidget(self.__boton)

        self.__boton.clicked.connect(self.__on_btn_registrar)

        self.setLayout(self.__contenedor)

    def __on_btn_registrar(self):
        self.__label_error.setStyleSheet("color: red")
        if self.__cbx_tipo_transaccion.currentIndex() == -1:
            self.__label_error.setText("Seleccione tipo de transaccion")
        elif self.__cbx_categorias.currentIndex() == -1:
            self.__label_error.setText("Seleccione categoria")
        else:
            self.registrar.emit()
        
    def __limpiar(self):
        self.__line_monto.clear()
        self.__cbx_tipo_transaccion.clear()
        self.__cbx_categorias.clear()
        self.__line_descripcion.clear()
        self.__label_error.setStyleSheet("color: gray")
        self.__label_error.setText("Campos con * obligatorios")
        self.__cal_fecha.setSelectedDate(QtCore.QDate.currentDate())
    
    def verificar_error(self, mensaje_error):
        if mensaje_error != None:
            self.__label_error.setStyleSheet("color: red")
            self.__label_error.setText(mensaje_error)
        else:
            self.__limpiar()
            self.close()

    def closeEvent(self, evnt):
        self.__limpiar()

    def configurar_menu_desplegable(self, tipos_transaccion, categorias):
        self.tipos, self.categorias = tipos_transaccion, categorias
        self.__cbx_tipo_transaccion.addItems([tipo[1] for tipo in self.tipos])
        self.__cbx_categorias.addItems([categoria[1] for categoria in self.categorias])

    def obtener_datos(self):
        monto = self.__line_monto.text()
        id_tipo = self.tipos[self.__cbx_tipo_transaccion.currentIndex()][0]
        id_categoria = self.categorias[self.__cbx_categorias.currentIndex()][0]
        descripcion = self.__line_descripcion.toPlainText()
        fecha = self.__cal_fecha.selectedDate().toString()
        return TransaccionDTO(monto, id_tipo, id_categoria, descripcion, fecha)

class VentanaIngreso(VentanaIngresoEgreso):
    def __init__(self, parent = None):
        VentanaIngresoEgreso.__init__(self)
        self.setWindowTitle("Ingreso")

class VentanaEgreso(VentanaIngresoEgreso):
    def __init__(self, parent = None):
        VentanaIngresoEgreso.__init__(self)
        self.setWindowTitle("Egreso")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = VentanaEgreso()
    def visualizar_datos():
        print(ventana.obtener_datos())
    ventana.show()
    ventana.registrar.connect(lambda: visualizar_datos())
    app.exec()