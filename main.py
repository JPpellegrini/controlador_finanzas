import sys
import os
from PyQt5 import QtWidgets
from controlador.principal import Controlador
from modelo.modelo import Database
from dotenv import load_dotenv
load_dotenv()

database = Database.get(os.getenv("MYSQL_USERNAME"), os.getenv("MYSQL_PASSWORD"))
app = QtWidgets.QApplication(sys.argv)
controlador = Controlador()

app.aboutToQuit.connect(database.close)
controlador.show_vista()
app.exec()