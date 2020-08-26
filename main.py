import sys
import os
from PyQt5 import QtWidgets
from controlador.principal import Controlador
from dotenv import load_dotenv
load_dotenv()

app = QtWidgets.QApplication(sys.argv)
controlador = Controlador(os.getenv("MYSQL_USERNAME"), os.getenv("MYSQL_PASSWORD"))

app.aboutToQuit.connect(controlador.cerrar_database)
controlador.show_vista()
app.exec()