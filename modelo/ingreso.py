from dataclasses import dataclass
from modelo.recursos import Database
from modelo.tipo_transaccion import ServiceTipoTransaccion
from modelo.categoria_ingreso import ServiceCategoriaIngreso


@dataclass
class IngresoDTO:
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


class ServiceIngreso:
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()
        self.srv_tipos = ServiceTipoTransaccion()
        self.srv_categorias = ServiceCategoriaIngreso()

    def registrar_ingreso(self, data: IngresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        self.cursor.execute(
            "INSERT INTO ingresos (id, monto, tipo, categoria_ingreso, descripcion, fecha) VALUES (%s, %s, %s, %s, %s, %s)",
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

    def editar_ingreso(self, data: IngresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        self.cursor.execute(
            "UPDATE ingresos SET monto=%s, tipo=%s, categoria_ingreso=%s, descripcion=%s, fecha=%s WHERE id = %s",
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

    def eliminar_ingreso(self, data: IngresoDTO):
        self.cursor.execute("DELETE FROM ingresos WHERE id = %s", data.id)
        self.database.commit()

    def obtener_ingresos(self):
        self.cursor.execute(
            "SELECT i.id, i.monto, t.nombre as tipo, c.nombre as categoria, i.descripcion, i.fecha FROM ingresos i JOIN\
             tipos_transaccion t ON i.tipo=t.id JOIN categorias_ingreso c ON i.categoria_ingreso=c.id"
        )
        return [
            IngresoDTO(
                ingreso["monto"],
                ingreso["tipo"],
                ingreso["categoria"],
                ingreso["descripcion"],
                ingreso["fecha"],
                ingreso["id"],
            )
            for ingreso in self.cursor.fetchall()
        ]

    def obtener_tipos_categorias(self):
        return dict(
            tipos=self.srv_tipos.obtener_tipos(),
            categorias=self.srv_categorias.obtener_cat_ingreso(),
        )
