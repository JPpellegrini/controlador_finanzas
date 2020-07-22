from dataclasses import dataclass
import pymysql

@dataclass
class MovimientoDTO:
    monto = float
    categoria = object
    descripcion = str
    fecha = str

@dataclass
class CategoriaDTO:
    nombre = str
    descripcion = str

class Database:
    def __init__(self):
        self.conexion = pymysql.connect(#database)
        self.cursor = self.db.cursor()
    
class Service:
    def __init__(self):
        self.database = Database()
