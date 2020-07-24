from dataclasses import dataclass
import pymysql

@dataclass
class TransaccionDTO:
    monto: float
    categoria: object
    descripcion: str
    fecha: str
    id_movimiento: int
    id_categoria: int

@dataclass
class MovimientoDTO:
    nombre: str
    descripcion: str

@dataclass
class CategoriaDTO:
    nombre: str
    descripcion: str


class Service:
    def __init__(self):
        self.conexion = pymysql.connect(host="localhost", port=3306, user="usuario",
                                        passwd="1234", db="finanzas")
        self.cursor = self.conexion.cursor()

    def registrar_movimiento(self, data = MovimientoDTO):
        self.cursor.execute(
            "INSERT INTO movimientos VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
        )
        self.conexion.commit()
        
    def registrar_categoria(self, tipo, data = CategoriaDTO):
        self.cursor.execute(
            "INSERT INTO categorias_{} VALUES (%s, %s, %s)".format(tipo), (None, data.nombre, data.descripcion)
        )
        self.conexion.commit()

    def calcular_valance(self):
        pass

    def cerrar_database(self):
        self.conexion.close()

if __name__ == "__main__":
    categoria = CategoriaDTO('juan', 'hola')
    modelo = Service()
    
    modelo.registrar_categoria("egreso", categoria)
    modelo.cerrar_database()