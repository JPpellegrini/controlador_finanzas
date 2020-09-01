import sys
import os
from PyQt5 import QtWidgets
from controlador.principal import ControladorPrincipal
from modelo.modelo import Database
from dotenv import load_dotenv
load_dotenv()


db_user = dict(
    username = os.getenv("MYSQL_USERNAME"),
    password = os.getenv("MYSQL_PASSWORD"),
)
database = Database.get(db_user["username"],db_user["password"])

app = QtWidgets.QApplication(sys.argv)
app.aboutToQuit.connect(database.close)
controlador = ControladorPrincipal()
controlador.show_vista()
app.exec()