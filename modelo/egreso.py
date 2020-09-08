from dataclasses import dataclass
from modelo.recursos import Database
from modelo.tipo_transaccion import ServiceTipoTransaccion
from modelo.categoria_egreso import ServiceCategoriaEgreso


@dataclass
class EgresoDTO:
    monto: str
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: str
    id: int = None


class MontoError(Exception):
    def __str__(self):
        return "Monto invalido"


class TipoError(Exception):
    def __str__(self):
        return "Tipo invalido"


class CategoriaError(Exception):
    def __str__(self):
        return "Categoria invalida"


class ServiceEgreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()
        self.svc_tipos = ServiceTipoTransaccion()
        self.svc_categorias = ServiceCategoriaEgreso()

    def registrar_egreso(self, data: EgresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        self.cursor.execute(
            "INSERT INTO egresos (id, monto, tipo, categoria_egreso, descripcion, fecha) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                data.id,
                data.monto,
                data.id_tipo_transaccion,
                data.id_categoria,
                data.descripcion,
                data.fecha,
            ),
        )
        self.database.commit()

    def editar_egreso(self, data: EgresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        self.cursor.execute(
            "UPDATE egresos SET monto=%s, tipo=%s, categoria_egreso=%s, descripcion=%s, fecha=%s WHERE id = %s",
            (
                data.monto,
                data.id_tipo_transaccion,
                data.id_categoria,
                data.descripcion,
                data.fecha,
                data.id,
            ),
        )
        self.database.commit()

    def eliminar_egreso(self, data: EgresoDTO):
        self.cursor.execute("DELETE FROM egresos WHERE id = %s", data.id)
        self.database.commit()

    def obtener_egresos(self):
        self.cursor.execute(
            "SELECT e.id, e.monto, t.nombre as tipo, c.nombre as categoria, e.descripcion, e.fecha FROM egresos e JOIN\
             tipos_transaccion t ON e.tipo=t.id JOIN categorias_egreso c ON e.categoria_egreso=c.id"
        )
        return [
            EgresoDTO(
                egreso["monto"],
                egreso["tipo"],
                egreso["categoria"],
                egreso["descripcion"],
                egreso["fecha"],
                egreso["id"],
            )
            for egreso in self.cursor.fetchall()
        ]

    def obtener_tipos_categorias(self):
        return dict(
            tipos=self.svc_tipos.obtener_tipos(),
            categorias=self.svc_categorias.obtener_cat_egreso(),
        )
