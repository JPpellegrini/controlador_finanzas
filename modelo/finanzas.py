from dataclasses import dataclass
import pymysql


@dataclass
class TransaccionDTO:
    monto: str
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
                "INSERT INTO tipos_transaccion VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.guardar()
        else: return "Ingrese el nombre"
    
    def editar(self, id, data = Tipo_transaccionDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "UPDATE tipos_transaccion SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"

    def eliminar(self, *ids):
        try:
            self.database.ejecutar(
                "DELETE FROM tipos_transaccion WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, tipo/s de transaccion en uso"
    
    def obtener_tipos(self):
        return self.database.ejecutar(
            "SELECT * FROM tipos_transaccion"
        ).fetchall()

class Service_categoria_ingreso():
    def __init__(self, database):
        self.database = database

    def registrar(self, data = CategoriaDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "INSERT INTO categorias_ingreso VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"
    
    def editar(self, id, data = CategoriaDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "UPDATE categorias_ingreso SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"

    def eliminar(self, *ids):
        try:
            self.database.ejecutar(
                "DELETE FROM categorias_ingreso WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, categoria/s en uso"
    
    def obtener_tipos(self):
        return self.database.ejecutar(
            "SELECT * FROM categorias_ingreso"
        ).fetchall()

class Service_categoria_egreso():
    def __init__(self, database):
        self.database = database

    def registrar(self, data = CategoriaDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "INSERT INTO categorias_egreso VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"
    
    def editar(self, id, data = CategoriaDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "UPDATE categorias_egreso SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.guardar()
        else : return "Ingrese el nombre"

    def eliminar(self, *ids):
        try:
            self.database.ejecutar(
                "DELETE FROM categorias_egreso WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, categoria/s en uso"
    
    def obtener_tipos(self):
        return self.database.ejecutar(
            "SELECT * FROM categorias_egreso"
        ).fetchall() 

class Service_ingreso:
    def __init__(self, database):
        self.database = database

    def registrar(self, data = CategoriaDTO):
        try:
            self.database.ejecutar(
                "INSERT INTO ingresos VALUES (%s, %s, %s, %s, %s, %s)",\
                (None, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, ingrese monto valido"
    
    def editar(self, id, data = CategoriaDTO):
        try:
            self.database.ejecutar(
                "UPDATE ingresos SET monto=%s, tipo=%s, categoria_ingreso=%s, descripcion=%s, fecha=%s WHERE id = %s",\
                (data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha, id)
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, ingrese monto valido"

    def eliminar(self, *ids):
        self.database.ejecutar(
            "DELETE FROM ingresos WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
        )
        self.database.guardar()
    
    def obtener_ingresos(self):
        return self.database.ejecutar(
            "SELECT i.id, i.monto, t.nombre, c.nombre, i.descripcion, i.fecha FROM ingresos i JOIN\
             tipos_transaccion t ON i.tipo=t.id JOIN categorias_ingreso c ON i.categoria_ingreso=c.id"
        ).fetchall()
    


if __name__ == "__main__":
    database = Database()
    service = Service_ingreso(database)
    ingreso = TransaccionDTO("", 1, 1, "asd", "hoy")

    print(service.obtener_ingresos())
    database.cerrar_database()