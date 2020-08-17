import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class Ventana_ingreso_egreso(QtWidgets.QDialog):
    signal = QtCore.pyqtSignal()

    def __init__(self, titulo, parent = None):
        QtWidgets.QDialog.__init__(self, parent)

        #CONFIG
        self.setWindowTitle(titulo)

        self.__setupUi()
    
    def __setupUi(self):
        self.__contenedor = QtWidgets.QVBoxLayout()

        #WIDGETS
        self.__line_monto = QtWidgets.QLineEdit()
        self.__cbx_movimientos = QtWidgets.QComboBox()
        self.__cbx_categorias = QtWidgets.QComboBox()
        self.__line_descripcion = QtWidgets.QTextEdit()
        self.__cal_fecha = QtWidgets.QCalendarWidget()
        self.__label_error = QtWidgets.QLabel("Campos con * obligatorios")
        self.__boton = QtWidgets.QPushButton("Aceptar")
        
        self.__line_monto.setPlaceholderText("Monto*")
        self.__cbx_movimientos.setPlaceholderText("Movimiento*")
        self.__cbx_categorias.setPlaceholderText("Categoria*")
        self.__line_descripcion.setPlaceholderText("Descripcion")
        self.__label_error.setStyleSheet("color: gray")
        
        self.__contenedor.addWidget(self.__line_monto)
        self.__contenedor.addWidget(self.__cbx_movimientos)
        self.__contenedor.addWidget(self.__cbx_categorias)
        self.__contenedor.addWidget(self.__line_descripcion)
        self.__contenedor.addWidget(self.__cal_fecha)
        self.__contenedor.addWidget(self.__label_error)
        self.__contenedor.addWidget(self.__boton)

        self.__boton.clicked.connect(self.__on_btn_registrar)

        self.setLayout(self.__contenedor)

    def __on_btn_registrar(self):
        self.signal.emit()

    def __limpiar(self):
        self.__line_monto.clear()
        self.__cbx_movimientos.clear()
        self.__cbx_categorias.clear()
        self.__line_descripcion.clear()
        self.__label_error.setStyleSheet("color: gray")
        self.__label_error.setText("Campos con * obligatorios")
        self.__cal_fecha.setSelectedDate(QtCore.QDate.currentDate())
    
    '''def __verificar_error(self):
        self.__label_error.setStyleSheet("color: red")
        try:
            int(self.__line_monto.text())
            if self.__cbx_movimientos.currentIndex() == -1:
                self.__label_error.setText("Seleccione movimiento")
                return False
            if self.__cbx_categorias.currentIndex() == -1:
                self.__label_error.setText("Seleccione categoria")
                return False
            return True
        except ValueError:
            self.__label_error.setText("Ingrese numeros solamente")
            return False'''

    def closeEvent(self, evnt):
        self.__limpiar()

    def configurar_menu_desplegable(self, movimientos, categorias):
        self.__cbx_movimientos.addItems(movimientos.values())
        self.__cbx_categorias.addItems(categorias.values())

    def obtener_datos(self):
        return self.__line_monto.text(), self.__cbx_movimientos.currentIndex(),\
        self.__cbx_categorias.currentIndex(),self.__line_descripcion.toPlainText(),\
        self.__cal_fecha.selectedDate().toString()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = Ventana_ingreso_egreso("ventana")
    def visualizar_datos():
        print(ventana.obtener_datos())
    ventana.show()
    ventana.signal.connect(lambda: visualizar_datos())
    app.exec()