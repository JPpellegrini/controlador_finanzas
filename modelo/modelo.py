import pymysql
from dataclasses import dataclass


class NombreError(Exception):
    def __str__(self):
        return "Ingrese nombre"

class MontoError(Exception):
    def __str__(self):
        return "Ingrese monto valido"

class TipoUsoError(Exception):
    def __str__(self):
        return "Error, tipo/s en uso"

class CategoriaUsoError(Exception):
    def __str__(self):
        return "Error, categoria/s en uso"


@dataclass
class TransaccionDTO:
    monto: str
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: str
    id: int=None

@dataclass
class TipoTransaccionDTO:
    nombre: str
    descripcion: str
    id: int=None

@dataclass
class CategoriaDTO:
    nombre: str
    descripcion: str
    id: int=None
   
class Database:
    __conexion = None

    @classmethod
    def get(cls, username = None, password = None): 
        if not cls.__conexion:  
            cls.__conexion = pymysql.connect(cursorclass=pymysql.cursors.DictCursor,host="localhost",
                                            port=3306, user=username, passwd=password, db="finanzas")
        return cls.__conexion
        

class Balance:
    @staticmethod
    def calcular():
        database = Database.get()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT SUM(monto) as total FROM ingresos")
            ingresos = cursor.fetchone()["total"]
            cursor.execute("SELECT SUM(monto) as total FROM egresos")
            egresos = cursor.fetchone()["total"]
            return ingresos - egresos
        except TypeError:
            if ingresos != None:
                return 0 + ingresos
            elif egresos != None:
                return 0 - egresos
            return 0


class ServiceTipoTransaccion:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar_tipo(self, data = TipoTransaccionDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "INSERT INTO tipos_transaccion (id, nombre, descripcion) VALUES (%s, %s, %s)", (data.id, data.nombre, data.descripcion)
        )
        self.database.commit() 
    
    def editar_tipo(self, data = TipoTransaccionDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "UPDATE tipos_transaccion SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, data.id)
        )
        self.database.commit()

    def eliminar_tipo(self, data = TipoTransaccionDTO):
        try:
            self.cursor.execute(
                "DELETE FROM tipos_transaccion WHERE id = %s", data.id
            )
            self.database.commit()
        except pymysql.Error:
            raise TipoUsoError
    
    def obtener_tipos(self):
        self.cursor.execute(
            "SELECT id, nombre, descripcion FROM tipos_transaccion"
        )
        return [TipoTransaccionDTO(tipo["nombre"], tipo["descripcion"], tipo["id"]) for tipo in self.cursor.fetchall()]


class ServiceCategoriaIngreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar_cat_ingreso(self, data = CategoriaDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "INSERT INTO categorias_ingreso (id, nombre, descripcion) VALUES (%s, %s, %s)", (data.id, data.nombre, data.descripcion)
        )
        self.database.commit()
            
    def editar_cat_ingreso(self, data = CategoriaDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "UPDATE categorias_ingreso SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, data.id)
        )
        self.database.commit()       

    def eliminar_cat_ingreso(self, data = CategoriaDTO):
        try:
            self.cursor.execute(
                "DELETE FROM categorias_ingreso WHERE id = %s", data.id
            )
            self.database.commit()
        except pymysql.Error:
            raise CategoriaUsoError
    
    def obtener_cat_ingreso(self):
        self.cursor.execute(
            "SELECT id, nombre, descripcion FROM categorias_ingreso"
        )
        return [CategoriaDTO(categoria["nombre"], categoria["descripcion"], categoria["id"]) for categoria in self.cursor.fetchall()]


class ServiceCategoriaEgreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar_cat_egreso(self, data = CategoriaDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "INSERT INTO categorias_egreso (id, nombre, descripcion) VALUES (%s, %s, %s)", (data.id, data.nombre, data.descripcion)
        )
        self.database.commit()
    
    def editar_cat_egreso(self, data = CategoriaDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "UPDATE categorias_egreso SET nombre=%s, descripcion=%s WHERE id = %s", (data.nombre, data.descripcion, data.id)
        )
        self.database.commit()

    def eliminar_cat_egreso(self, data = CategoriaDTO):
        try:
            self.cursor.execute(
                "DELETE FROM categorias_egreso WHERE id = %s", data.id
            )
            self.database.commit()
        except pymysql.Error:
            raise CategoriaUsoError
    
    def obtener_cat_egreso(self):
        self.cursor.execute(
            "SELECT id, nombre, descripcion FROM categorias_egreso"
        )
        return [CategoriaDTO(categoria["nombre"], categoria["descripcion"], categoria["id"]) for categoria in self.cursor.fetchall()]


class ServiceIngreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()
        self.srv_tipos = ServiceTipoTransaccion()
        self.srv_categorias = ServiceCategoriaIngreso()

    def registrar_ingreso(self, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "INSERT INTO ingresos (id, monto, tipo, categoria_ingreso, descripcion, fecha) VALUES (%s, %s, %s, %s, %s, %s)",\
                (data.id, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.commit()
        except pymysql.Error:
            raise MontoError
    
    def editar_ingreso(self, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "UPDATE ingresos SET monto=%s, tipo=%s, categoria_ingreso=%s, descripcion=%s, fecha=%s WHERE id = %s",\
                (data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha, data.id)
            )
            self.database.commit()
        except pymysql.Error:
            raise MontoError

    def eliminar_ingreso(self, data = TransaccionDTO):
        self.cursor.execute(
            "DELETE FROM ingresos WHERE id = %s", data.id
        )
        self.database.commit()
    
    def obtener_ingresos(self):
        self.cursor.execute(
            "SELECT i.id, i.monto, t.nombre as tipo, c.nombre as categoria, i.descripcion, i.fecha FROM ingresos i JOIN\
             tipos_transaccion t ON i.tipo=t.id JOIN categorias_ingreso c ON i.categoria_ingreso=c.id"
        )
        return [TransaccionDTO(transaccion["monto"], transaccion["tipo"], transaccion["categoria"], transaccion["descripcion"], transaccion["fecha"], transaccion["id"]) for transaccion in self.cursor.fetchall()]
    
    def obtener_tipos_categorias(self):
        return dict(tipos = self.srv_tipos.obtener_tipos(), categorias = self.srv_categorias.obtener_cat_ingreso())


class ServiceEgreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()
        self.svc_tipos = ServiceTipoTransaccion()
        self.svc_categorias = ServiceCategoriaEgreso()

    def registrar_egreso(self, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "INSERT INTO egresos (id, monto, tipo, categoria_egreso, descripcion, fecha) VALUES (%s, %s, %s, %s, %s, %s)",\
                (data.id, data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha)
            )
            self.database.commit()
        except pymysql.Error:
            raise MontoError
    
    def editar_egreso(self, data = TransaccionDTO):
        try:
            self.cursor.execute(
                "UPDATE egresos SET monto=%s, tipo=%s, categoria_egreso=%s, descripcion=%s, fecha=%s WHERE id = %s",\
                (data.monto, data.id_tipo_transaccion, data.id_categoria, data.descripcion, data.fecha, data.id)
            )
            self.database.commit()
        except pymysql.Error:
            raise MontoError

    def eliminar_egreso(self, data = TransaccionDTO):
        self.cursor.execute(
            "DELETE FROM egresos WHERE id = %s", data.id
        )
        self.database.commit()
    
    def obtener_egresos(self):
        self.cursor.execute(
            "SELECT e.id, e.monto, t.nombre as tipo, c.nombre as categoria, e.descripcion, e.fecha FROM egresos e JOIN\
             tipos_transaccion t ON e.tipo=t.id JOIN categorias_egreso c ON e.categoria_egreso=c.id"
        )
        return [TransaccionDTO(transaccion["monto"], transaccion["tipo"], transaccion["categoria"], transaccion["descripcion"], transaccion["fecha"], transaccion["id"]) for transaccion in self.cursor.fetchall()]

    def obtener_tipos_categorias(self):
        return dict(tipos = self.svc_tipos.obtener_tipos(), categorias = self.svc_categorias.obtener_cat_egreso())


if __name__ == "__main__":
    Database.get("usuario", "1234")
    service = ServiceEgreso()
    tipo = TipoTransaccionDTO("tarjeta", "xd")
    
    print(service.obtener_egresos())
    Database.get().close()