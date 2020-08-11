from dataclasses import dataclass
import pymysql


@dataclass
class TransaccionDTO:
    monto: float
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: str

@dataclass
class Tipo_transaccionDTO:
    nombre: str
    descripcion: str

@dataclass
class CategoriaDTO:
    nombre: str
    descripcion: str

class Database:
    def __init__(self):
        self.conexion = pymysql.connect(host="localhost", port=3306, user="usuario",
                                        passwd="1234", db="finanzas")
        self.cursor = self.conexion.cursor()
    
    def cerrar_database(self):
        self.conexion.close()