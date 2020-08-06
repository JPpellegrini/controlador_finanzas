import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class Ventana_movimiento_categoria(QtWidgets.QDialog):
    signal= QtCore.pyqtSignal()

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
        self.__limpiar()
        self.close()
    
    def __limpiar(self):
        self.__line_nombre.setText("")
        self.__line_descripcion.setText("")
    
    def closeEvent(self, evnt):
        self.__limpiar()

    def obtener_datos(self):
        return self.__line_nombre.text(), self.__line_descripcion.toPlainText()

class Ventana_ingresos_egreso(QtWidgets.QDialog):
    signal = QtCore.pyqtSignal()

    def __init__(self, parent = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.__setupUi()
    
    def __setupUi(self):
        self.__contenedor = QtWidgets.QVBoxLayout()

        #WIDGETS
        self.__line_monto = QtWidgets.QLineEdit()
        self.__cbx_movimientos = QtWidgets.QComboBox()
        self.__cbx_categorias = QtWidgets.QComboBox()
        self.__line_descripcion = QtWidgets.QTextEdit()
        self.__cal_fecha = QtWidgets.QCalendarWidget()
        self.__boton = QtWidgets.QPushButton("Aceptar")
        
        self.__line_monto.setPlaceholderText("Monto")
        self.__cbx_movimientos.setPlaceholderText("Movimiento")
        self.__cbx_categorias.setPlaceholderText("Categoria")
        self.__line_descripcion.setPlaceholderText("Descripcion")
        
        self.__contenedor.addWidget(self.__line_monto)
        self.__contenedor.addWidget(self.__cbx_movimientos)
        self.__contenedor.addWidget(self.__cbx_categorias)
        self.__contenedor.addWidget(self.__line_descripcion)
        self.__contenedor.addWidget(self.__cal_fecha)
        self.__contenedor.addWidget(self.__boton)

        self.__boton.clicked.connect(self.__on_btn_registrar)

        self.setLayout(self.__contenedor)

    def __on_btn_registrar(self):
        self.signal.emit()
        self.__limpiar()
        self.close()

    def __limpiar(self):
        self.__line_monto.setText("")
        self.__cbx_movimientos.clear()
        self.__cbx_categorias.clear()
        self.__line_descripcion.setText("")
        self.__cal_fecha.setSelectedDate(QtCore.QDate.currentDate())

    def closeEvent(self, evnt):
        self.__limpiar()

    def configurar_menu_desplegable(self, movimientos, categorias):
        self.__cbx_movimientos.addItems(movimientos.values())
        self.__cbx_categorias.addItems(categorias.values())

    def obtener_datos(self):
        return self.__line_monto.text(), self.__cbx_movimientos.currentIndex(),\
        self.__cbx_categorias.currentIndex(),self.__line_descripcion.toPlainText(),\
        self.__cal_fecha.selectedDate().toString()
        


class Vista(QtWidgets.QWidget):
    
    calcular_balance = QtCore.pyqtSignal()
    agregar_ingreso = QtCore.pyqtSignal()
    agregar_egreso = QtCore.pyqtSignal()
    agregar_movimiento = QtCore.pyqtSignal()
    agregar_categoria_ingreso = QtCore.pyqtSignal()
    agregar_categoria_egreso = QtCore.pyqtSignal()
    actualizar_mov_cat_ingreso = QtCore.pyqtSignal()
    actualizar_mov_cat_egreso = QtCore.pyqtSignal()


    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.ventana_agregar_ingreso = Ventana_ingresos_egreso()
        self.ventana_agregar_egreso = Ventana_ingresos_egreso()
        self.ventana_agregar_movimiento = Ventana_movimiento_categoria()
        self.ventana_agregar_categoria_ingreso = Ventana_movimiento_categoria()
        self.ventana_agregar_categoria_egreso = Ventana_movimiento_categoria()

        self.ventana_agregar_categoria_egreso.signal.connect(lambda: self.agregar_categoria_egreso.emit())
        self.ventana_agregar_categoria_ingreso.signal.connect(lambda: self.agregar_categoria_ingreso.emit())
        self.ventana_agregar_movimiento.signal.connect(lambda: self.agregar_movimiento.emit())
        self.ventana_agregar_ingreso.signal.connect(lambda: [signal.emit() for signal in (self.agregar_ingreso, self.calcular_balance)])
        self.ventana_agregar_egreso.signal.connect(lambda: [signal.emit() for signal in (self.agregar_egreso, self.calcular_balance)])

        self.__setupUi()

    def __setupUi(self):
        self.__layout = QtWidgets.QFormLayout()

        #WIDGETS
        self.__label_balance = QtWidgets.QLabel('$0')
        self.__btn_ingreso = QtWidgets.QPushButton("Nuevo Ingreso")
        self.__btn_egreso = QtWidgets.QPushButton("Nuevo Egreso")
        self.__btn_movimiento = QtWidgets.QPushButton("Nuevo Movimiento")
        self.__btn_categoria_ingreso = QtWidgets.QPushButton("Nueva Categoria Ingreso")
        self.__btn_categoria_egreso = QtWidgets.QPushButton("Nueva Categoria Egreso")
        self.__calendario = QtWidgets.QCalendarWidget()
        
        self.__layout.addRow("Balance: ", self.__label_balance)
        self.__layout.addRow(self.__btn_ingreso)
        self.__layout.addRow(self.__btn_egreso)
        self.__layout.addRow(self.__btn_movimiento)
        self.__layout.addRow(self.__btn_categoria_ingreso)
        self.__layout.addRow(self.__btn_categoria_egreso)
        self.__layout.addRow(self.__calendario)

        self.__btn_ingreso.clicked.connect(self.__on_btn_ingreso_clicked)
        self.__btn_egreso.clicked.connect(self.__on_btn_egreso_clicked)
        self.__btn_movimiento.clicked.connect(self.__on_btn_movimiento_clicked)
        self.__btn_categoria_ingreso.clicked.connect(self.__on_btn_categoria_ingreso_clicked)
        self.__btn_categoria_egreso.clicked.connect(self.__on_btn_categoria_egreso_clicked)
                
        self.setLayout(self.__layout)
    
    def __on_btn_ingreso_clicked(self):
        self.actualizar_mov_cat_ingreso.emit()
        self.ventana_agregar_ingreso.exec()

    def __on_btn_egreso_clicked(self):
        self.actualizar_mov_cat_egreso.emit()
        self.ventana_agregar_egreso.exec()

    def __on_btn_movimiento_clicked(self):
        self.ventana_agregar_movimiento.exec_()

    def __on_btn_categoria_ingreso_clicked(self):
        self.ventana_agregar_categoria_ingreso.exec_()

    def __on_btn_categoria_egreso_clicked(self):
        self.ventana_agregar_categoria_egreso.exec_()

    def actualizar_balance(self, valor):
        self.__label_balance.setText(str(valor))

if __name__ == "__main__":
    def fun():
        datos = vista.ventana_agregar_ingreso.obtener_datos()
        id = list(men1.values())
        print(id[datos[3]])

    app = QtWidgets.QApplication(sys.argv)
    vista = Vista()
    men1 = {"hola": 0, "camaleon": 1}
    men2 = {"pantufla": 0, "ladrillo": 1}
    vista.ventana_agregar_ingreso.configurar_menu_desplegable(men1, men2)
    vista.agregar_ingreso.connect(fun)
    vista.show()
    app.exec()