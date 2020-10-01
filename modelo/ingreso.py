import sys

sys.path.append("..")
from dataclasses import dataclass
from modelo.recursos import Session, Ingreso
from modelo.tipo_transaccion import ServiceTipoTransaccion
from modelo.categoria_ingreso import ServiceCategoriaIngreso
from datetime import datetime, date


@dataclass
class FiltroDTO:
    fecha: date = None


@dataclass
class IngresoDTO:
    monto: str
    id_tipo_transaccion: int
    id_categoria: int
    descripcion: str
    fecha: datetime
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
    def registrar_ingreso(self, data: IngresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        session = Session()
        ingreso = Ingreso(
            id=data.id,
            monto=data.monto,
            id_tipo_transaccion=data.id_tipo_transaccion,
            id_categoria=data.id_categoria,
            descripcion=data.descripcion,
            fecha=data.fecha,
        )
        session.add(ingreso)
        session.commit()

    def editar_ingreso(self, data: IngresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        session = Session()
        ingreso = session.query(Ingreso).filter_by(id=data.id).first()
        ingreso.monto = (data.monto,)
        ingreso.id_tipo_transaccion = (data.id_tipo_transaccion,)
        ingreso.id_categoria = (data.id_categoria,)
        ingreso.descripcion = (data.descripcion,)
        ingreso.fecha = (data.fecha,)
        session.commit()

    def eliminar_ingreso(self, data: IngresoDTO):
        session = Session()
        ingreso = session.query(Ingreso).filter_by(id=data.id).first()
        session.delete(ingreso)
        session.commit()

    def obtener_ingresos(self, filtro: FiltroDTO = FiltroDTO()):
        condiciones = {}
        if filtro.fecha:
            condiciones["fecha"] = filtro.fecha
        session = Session()
        ingresos = session.query(Ingreso).filter_by(**condiciones)

        return [
            IngresoDTO(
                ingreso.monto,
                ingreso.id_tipo_transaccion,
                ingreso.id_categoria,
                ingreso.descripcion,
                ingreso.fecha,
                ingreso.id,
            )
            for ingreso in ingresos
        ]
