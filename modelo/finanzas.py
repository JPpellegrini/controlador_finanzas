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
        self.__conexion = pymysql.connect(host="localhost", port=3306, user="usuario",
                                        passwd="1234", db="finanzas")
        self.__cursor = self.__conexion.cursor()
    
    def ejecutar(self, sentencia, argumentos = None):
        self.__cursor.execute(sentencia, argumentos)
        return self.__cursor
    
    def guardar(self):
        self.__conexion.commit()
    
    def cerrar_database(self):
        self.__conexion.close()

class Service_tipo_transaccion():
    def __init__(self, database):
        self.database = database

    def registrar(self, data = Tipo_transaccionDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "INSERT INTO movimientos VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"
    
    def editar(self, id, data = Tipo_transaccionDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "UPDATE movimientos SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"

    def eliminar(self, id):
        self.database.ejecutar(
            "DELETE FROM movimientos WHERE id = %s", (id)
        )
        self.database.guardar()
    
    def obtener_tipos(self):
        return self.database.ejecutar(
            "SELECT * FROM movimientos"
        ).fetchall()
    
if __name__ == "__main__":
    database = Database()
    service = Service_tipo_transaccion(database)
    tipo1 = Tipo_transaccionDTO("prueba", "comentario")