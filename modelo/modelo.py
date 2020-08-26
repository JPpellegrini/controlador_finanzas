import pymysql
from dataclasses import dataclass


@dataclass
class TransaccionDTO:
    monto: str
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: str

@dataclass
class TipoTransaccionDTO:
    nombre: str
    descripcion: str

@dataclass
class CategoriaDTO:
    nombre: str
    descripcion: str

class Database:
    def __init__(self, username, password):
        self.__conexion = pymysql.connect(host="localhost", port=3306, user=username,
                                        passwd=password, db="finanzas")
        self.__cursor = self.__conexion.cursor()
    
    def ejecutar(self, sentencia, argumentos = None):
        self.__cursor.execute(sentencia, argumentos)
        return self.__cursor
    
    def guardar(self):
        self.__conexion.commit()
    
    def cerrar(self):
        self.__conexion.close()
        

class Balance:
    @staticmethod
    def calcular(database):
        try:
            ingresos = database.ejecutar("SELECT SUM(monto) FROM ingresos").fetchone()[0]
            egresos = database.ejecutar("SELECT SUM(monto) FROM egresos").fetchone()[0]
            return ingresos - egresos
        except TypeError:
            if ingresos != None: return 0 + ingresos
            elif egresos != None: return 0 - egresos
            else: return 0


class ServiceTipoTransaccion:
    def __init__(self, database):
        self.database = database

    def registrar(self, data = TipoTransaccionDTO):
        if data.nombre != "":
            self.database.ejecutar(
                "INSERT INTO tipos_transaccion VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.guardar()
        else: return "Ingrese el nombre"
    
    def editar(self, id, data = TipoTransaccionDTO):
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


class ServiceCategoriaIngreso:
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
    
    def obtener_categorias(self):
        return self.database.ejecutar(
            "SELECT * FROM categorias_ingreso"
        ).fetchall()


class ServiceCategoriaEgreso:
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
    
    def obtener_categorias(self):
        return self.database.ejecutar(
            "SELECT * FROM categorias_egreso"
        ).fetchall() 


class ServiceIngreso:
    def __init__(self, database):
        self.database = database
        self.srv_tipos = ServiceTipoTransaccion(self.database)
        self.srv_categorias = ServiceCategoriaIngreso(self.database)

    def registrar(self, data = TransaccionDTO):
        try:
            self.database.ejecutar(
                "INSERT INTO ingresos VALUES (%s, %s, %s, %s, %s, %s)",\
                (None, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, ingrese monto valido"
    
    def editar(self, id, data = TransaccionDTO):
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
    
    def obtener_tipos_categorias(self):
        return self.srv_tipos.obtener_tipos(), self.srv_categorias.obtener_categorias()


class ServiceEgreso:
    def __init__(self, database):
        self.database = database
        self.svc_tipos = ServiceTipoTransaccion(self.database)
        self.svc_categorias = ServiceCategoriaEgreso(self.database)

    def registrar(self, data = TransaccionDTO):
        try:
            self.database.ejecutar(
                "INSERT INTO egresos VALUES (%s, %s, %s, %s, %s, %s)",\
                (None, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, ingrese monto valido"
    
    def editar(self, id, data = TransaccionDTO):
        try:
            self.database.ejecutar(
                "UPDATE egresos SET monto=%s, tipo=%s, categoria_egreso=%s, descripcion=%s, fecha=%s WHERE id = %s",\
                (data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha, id)
            )
            self.database.guardar()
        except pymysql.Error:
            return "Error, ingrese monto valido"

    def eliminar(self, *ids):
        self.database.ejecutar(
            "DELETE FROM egresos WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
        )
        self.database.guardar()
    
    def obtener_egresos(self):
        return self.database.ejecutar(
            "SELECT e.id, e.monto, t.nombre, c.nombre, e.descripcion, e.fecha FROM egresos e JOIN\
             tipos_transaccion t ON e.tipo=t.id JOIN categorias_egreso c ON e.categoria_ingreso=c.id"
        ).fetchall()

    def obtener_tipos_categorias(self):
        return self.svc_tipos.obtener_tipos(), self.svc_categorias.obtener_categorias()


if __name__ == "__main__":
    database = Database()
    service = ServiceIngreso(database)
    ingreso = TransaccionDTO("", 1, 1, "asd", "hoy")

    print(Balance.calcular(database))
    database.cerrar()