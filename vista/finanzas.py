import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class Ventana_movimiento_categoria(QtWidgets.QDialog):
    signal= QtCore.pyqtSignal()

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
        if self.__verificar_error():
            self.signal.emit()
            self.__limpiar()
            self.close()
    
    def __limpiar(self):
        self.__line_nombre.clear()
        self.__line_descripcion.clear()
        self.__label_error.setStyleSheet("color: gray")
        self.__label_error.setText("Campos con * obligatorios")
    
    def __verificar_error(self):
        self.__label_error.setStyleSheet("color: red")
        if self.__line_nombre.text() == "":
            self.__label_error.setText("Ingrese un nombre")
            return False
        else: return True

    def closeEvent(self, evnt):
        self.__limpiar()

    def obtener_datos(self):
        return self.__line_nombre.text(), self.__line_descripcion.toPlainText()

class Ventana_ingresos_egreso(QtWidgets.QDialog):
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
        if self.__verificar_error():
            self.signal.emit()
            self.__limpiar()
            self.close()

    def __limpiar(self):
        self.__line_monto.clear()
        self.__cbx_movimientos.clear()
        self.__cbx_categorias.clear()
        self.__line_descripcion.clear()
        self.__label_error.setStyleSheet("color: gray")
        self.__label_error.setText("Campos con * obligatorios")
        self.__cal_fecha.setSelectedDate(QtCore.QDate.currentDate())
    
    def __verificar_error(self):
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
            return False

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
    
    #SIGNALS
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

        #CONFIG
        self.setWindowTitle("Controlador de Finanzas")

        #VENTANAS
        self.ventana_agregar_ingreso = Ventana_ingresos_egreso("Ingreso")
        self.ventana_agregar_egreso = Ventana_ingresos_egreso("Egreso")
        self.ventana_agregar_movimiento = Ventana_movimiento_categoria("Movimiento")
        self.ventana_agregar_categoria_ingreso = Ventana_movimiento_categoria("Categoria de Ingreso")
        self.ventana_agregar_categoria_egreso = Ventana_movimiento_categoria("Categoria de Engreso")

        self.ventana_agregar_categoria_egreso.signal.connect(lambda: self.agregar_categoria_egreso.emit())
        self.ventana_agregar_categoria_ingreso.signal.connect(lambda: self.agregar_categoria_ingreso.emit())
        self.ventana_agregar_movimiento.signal.connect(lambda: self.agregar_movimiento.emit())
        self.ventana_agregar_ingreso.signal.connect(lambda: [signal.emit() for signal in (self.agregar_ingreso, self.calcular_balance)])
        self.ventana_agregar_egreso.signal.connect(lambda: [signal.emit() for signal in (self.agregar_egreso, self.calcular_balance)])

        self.__setupUi()

    def __setupUi(self):
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__btn_layout = QtWidgets.QVBoxLayout()
        self.__cal_layout = QtWidgets.QVBoxLayout()
        self.__opcion_layout = QtWidgets.QHBoxLayout()

        #WIDGETS
        self.__line_balance = QtWidgets.QLineEdit()
        self.__btn_ingreso = QtWidgets.QPushButton("Nuevo Ingreso")
        self.__btn_egreso = QtWidgets.QPushButton("Nuevo Egreso")
        self.__btn_movimiento = QtWidgets.QPushButton("Nuevo Movimiento")
        self.__btn_categoria_ingreso = QtWidgets.QPushButton("Nueva Categoria de Ingreso")
        self.__btn_categoria_egreso = QtWidgets.QPushButton("Nueva Categoria de Egreso")
        self.__calendario = QtWidgets.QCalendarWidget()
        self.__label_ingresos = QtWidgets.QLabel('Ingresos')
        self.__tree_ingresos = QtWidgets.QTreeView()
        self.__label_egresos = QtWidgets.QLabel('Egresos')
        self.__tree_egresos = QtWidgets.QTreeView()
        self.__btn_editar = QtWidgets.QPushButton("Editar")
        self.__btn_eliminar = QtWidgets.QPushButton("Eliminar")

        #CONFIG WIDGETS
        self.__line_balance.setReadOnly(1)
        self.__btn_editar.setEnabled(False)
        self.__btn_eliminar.setEnabled(False)
        self.__label_ingresos.setStyleSheet("color: green")
        self.__label_egresos.setStyleSheet("color: red")

        #IPLEMENTACION WIDGETS
        self.__main_layout.addLayout(self.__btn_layout)
        self.__main_layout.addLayout(self.__cal_layout)
        
        self.__btn_layout.addWidget(self.__btn_ingreso)
        self.__btn_layout.addWidget(self.__btn_egreso)
        self.__btn_layout.addWidget(self.__btn_movimiento)
        self.__btn_layout.addWidget(self.__btn_categoria_ingreso)
        self.__btn_layout.addWidget(self.__btn_categoria_egreso)
        self.__btn_layout.addWidget(self.__line_balance)

        self.__cal_layout.addWidget(self.__calendario)
        self.__cal_layout.addWidget(self.__label_ingresos)
        self.__cal_layout.addWidget(self.__tree_ingresos)
        self.__cal_layout.addWidget(self.__label_egresos)
        self.__cal_layout.addWidget(self.__tree_egresos)

        self.__btn_layout.addLayout(self.__opcion_layout)
        self.__opcion_layout.addWidget(self.__btn_editar)
        self.__opcion_layout.addWidget(self.__btn_eliminar)

        #BOTONES
        self.__btn_ingreso.clicked.connect(self.__on_btn_ingreso_clicked)
        self.__btn_egreso.clicked.connect(self.__on_btn_egreso_clicked)
        self.__btn_movimiento.clicked.connect(self.__on_btn_movimiento_clicked)
        self.__btn_categoria_ingreso.clicked.connect(self.__on_btn_categoria_ingreso_clicked)
        self.__btn_categoria_egreso.clicked.connect(self.__on_btn_categoria_egreso_clicked)
                
        self.setLayout(self.__main_layout)
    
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
        self.__line_balance.setText("Balance: " + str(valor))