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
    __conexion = None

    @classmethod
    def get(cls, username = None, password = None): 
        if not cls.__conexion:  
            cls.__conexion = pymysql.connect(host="localhost", port=3306, user=username,
                                        passwd=password, db="finanzas")
        return cls.__conexion
        

class Balance:
    @staticmethod
    def calcular():
        database = Database.get()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT SUM(monto) FROM ingresos")
            ingresos = cursor.fetchone()[0] 
            cursor.execute("SELECT SUM(monto) FROM egresos")
            egresos = cursor.fetchone()[0]
            return ingresos - egresos
        except TypeError:
            if ingresos != None:
                return 0 + ingresos
            elif egresos != None:
                return 0 - egresos
            else:
                return 0


class ServiceTipoTransaccion:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar(self, data = TipoTransaccionDTO):
        if data.nombre != "":
            self.cursor.execute(
                "INSERT INTO tipos_transaccion VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.commit()
        else: 
            return "Ingrese el nombre"
    
    def editar(self, id, data = TipoTransaccionDTO):
        if data.nombre != "":
            self.cursor.execute(
                "UPDATE tipos_transaccion SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.commit()
        else:
            return "Ingrese el nombre"

    def eliminar(self, *ids):
        try:
            self.cursor.execute(
                "DELETE FROM tipos_transaccion WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, tipo/s de transaccion en uso"
    
    def obtener_tipos(self):
        self.cursor.execute(
            "SELECT * FROM tipos_transaccion"
        )
        return [TipoTransaccionDTO(tipo[1], tipo[2]) for tipo in self.cursor.fetchall()]


class ServiceCategoriaIngreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar(self, data = CategoriaDTO):
        if data.nombre != "":
            self.cursor.execute(
                "INSERT INTO categorias_ingreso VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.commit()
        else: 
            return "Ingrese el nombre"
    
    def editar(self, id, data = CategoriaDTO):
        if data.nombre != "":
            self.cursor.execute(
                "UPDATE categorias_ingreso SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.commit()
        else:
            return "Ingrese el nombre"

    def eliminar(self, *ids):
        try:
            self.cursor.execute(
                "DELETE FROM categorias_ingreso WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, categoria/s en uso"
    
    def obtener_categorias(self):
        self.cursor.execute(
            "SELECT * FROM categorias_ingreso"
        )
        return [CategoriaDTO(categoria[1], categoria[2]) for categoria in self.cursor.fetchall()]


class ServiceCategoriaEgreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar(self, data = CategoriaDTO):
        if data.nombre != "":
            self.cursor.execute(
                "INSERT INTO categorias_egreso VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
            )
            self.database.commit()
        else:
            return "Ingrese el nombre"
    
    def editar(self, id, data = CategoriaDTO):
        if data.nombre != "":
            self.cursor.execute(
                "UPDATE categorias_egreso SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, id)
            )
            self.database.commit()
        else:
            return "Ingrese el nombre"

    def eliminar(self, *ids):
        try:
            self.cursor.execute(
                "DELETE FROM categorias_egreso WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, categoria/s en uso"
    
    def obtener_categorias(self):
        self.cursor.execute(
            "SELECT * FROM categorias_egreso"
        )
        return [CategoriaDTO(categoria[1], categoria[2]) for categoria in self.cursor.fetchall()]


class ServiceIngreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()
        self.srv_tipos = ServiceTipoTransaccion()
        self.srv_categorias = ServiceCategoriaIngreso()

    def registrar(self, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "INSERT INTO ingresos VALUES (%s, %s, %s, %s, %s, %s)",\
                (None, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, ingrese monto valido"
    
    def editar(self, id, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "UPDATE ingresos SET monto=%s, tipo=%s, categoria_ingreso=%s, descripcion=%s, fecha=%s WHERE id = %s",\
                (data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha, id)
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, ingrese monto valido"

    def eliminar(self, *ids):
        self.cursor.execute(
            "DELETE FROM ingresos WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
        )
        self.database.commit()
    
    def obtener_ingresos(self):
        self.cursor.execute(
            "SELECT i.id, i.monto, t.nombre, c.nombre, i.descripcion, i.fecha FROM ingresos i JOIN\
             tipos_transaccion t ON i.tipo=t.id JOIN categorias_ingreso c ON i.categoria_ingreso=c.id"
        )
        return [TransaccionDTO(transaccion[1], transaccion[2], transaccion[3], transaccion[4], transaccion[5]) for transaccion in self.cursor.fetchall()]
    
    def obtener_tipos_categorias(self):
        return self.srv_tipos.obtener_tipos(), self.srv_categorias.obtener_categorias()


class ServiceEgreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()
        self.svc_tipos = ServiceTipoTransaccion()
        self.svc_categorias = ServiceCategoriaEgreso()

    def registrar(self, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "INSERT INTO egresos VALUES (%s, %s, %s, %s, %s, %s)",\
                (None, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, ingrese monto valido"
    
    def editar(self, id, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "UPDATE egresos SET monto=%s, tipo=%s, categoria_egreso=%s, descripcion=%s, fecha=%s WHERE id = %s",\
                (data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha, id)
            )
            self.database.commit()
        except pymysql.Error:
            return "Error, ingrese monto valido"

    def eliminar(self, *ids):
        self.cursor.execute(
            "DELETE FROM egresos WHERE id IN ({})".format(('%s,'*len(ids))[:-1]), ids
        )
        self.database.commit()
    
    def obtener_egresos(self):
        self.cursor.execute(
            "SELECT e.id, e.monto, t.nombre, c.nombre, e.descripcion, e.fecha FROM egresos e JOIN\
             tipos_transaccion t ON e.tipo=t.id JOIN categorias_egreso c ON e.categoria_egreso=c.id"
        )
        return [TransaccionDTO(transaccion[1], transaccion[2], transaccion[3], transaccion[4], transaccion[5]) for transaccion in self.cursor.fetchall()]

    def obtener_tipos_categorias(self):
        return self.svc_tipos.obtener_tipos(), self.svc_categorias.obtener_categorias()


if __name__ == "__main__":
    Database.get("usuario", "1234")
    service = ServiceEgreso()
    tipo = TipoTransaccionDTO("tarjeta", "xd")
    
    print(service.obtener_egresos())
    Database.get().close()