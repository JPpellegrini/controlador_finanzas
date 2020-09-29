from dataclasses import dataclass
from app.modelo.recursos import Database


@dataclass
class TipoTransaccionDTO:
    nombre: str
    descripcion: str
    id: int = None


class NombreError(Exception):
    def __str__(self):
        return "Nombre invalido"


class TipoUsoError(Exception):
    def __str__(self):
        return "Error, tipo/s en uso"


class ServiceTipoTransaccion:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar_tipo(self, data: TipoTransaccionDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "INSERT INTO tipos_transaccion (id, nombre, descripcion) VALUES (%s, %s, %s)",
            (data.id, data.nombre, data.descripcion),
        )
        self.database.commit()

    def editar_tipo(self, data: TipoTransaccionDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "UPDATE tipos_transaccion SET nombre=%s, descripcion=%s WHERE id = %s",
            (data.nombre, data.descripcion, data.id),
        )
        self.database.commit()

    def eliminar_tipo(self, data: TipoTransaccionDTO):
        try:
            self.cursor.execute("DELETE FROM tipos_transaccion WHERE id = %s", data.id)
            self.database.commit()
        except pymysql.Error:
            raise TipoUsoError

    def obtener_tipos(self):
        self.cursor.execute("SELECT id, nombre, descripcion FROM tipos_transaccion")
        return [
            TipoTransaccionDTO(tipo["nombre"], tipo["descripcion"], tipo["id"])
            for tipo in self.cursor.fetchall()
        ]
