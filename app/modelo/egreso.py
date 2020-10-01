from dataclasses import dataclass
from datetime import datetime, date

from sqlalchemy import func

from app.modelo.recursos import Session, Egreso


@dataclass
class FiltroDTO:
    fecha: date = None


@dataclass
class EgresoDTO:
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


class ServiceEgreso:
    def registrar_egreso(self, data: EgresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        session = Session()
        egreso = Egreso(
            id=data.id,
            monto=data.monto,
            id_tipo_transaccion=data.id_tipo_transaccion,
            id_categoria=data.id_categoria,
            descripcion=data.descripcion,
            fecha=data.fecha,
        )
        session.add(egreso)
        session.commit()

    def editar_egreso(self, data: EgresoDTO):
        try:
            float(data.monto)
        except ValueError:
            raise MontoError
        if not data.id_tipo_transaccion:
            raise TipoError
        if not data.id_categoria:
            raise CategoriaError
        session = Session()
        egreso = session.query(Egreso).filter_by(id=data.id).first()
        egreso.monto = (data.monto,)
        egreso.id_tipo_transaccion = (data.id_tipo_transaccion,)
        egreso.id_categoria = (data.id_categoria,)
        egreso.descripcion = (data.descripcion,)
        egreso.fecha = (data.fecha,)
        session.commit()

    def eliminar_egreso(self, data: EgresoDTO):
        session = Session()
        egreso = session.query(Egreso).filter_by(id=data.id).first()
        session.delete(egreso)
        session.commit()

    def obtener_egresos(self, filtro: FiltroDTO = FiltroDTO()):
        condiciones = []
        if filtro.fecha:
            condiciones.append(func.date(Egreso.fecha)==filtro.fecha)
        session = Session()
        egresos = session.query(Egreso).filter(*condiciones)

        return [
            EgresoDTO(
                egreso.monto,
                egreso.id_tipo_transaccion,
                egreso.id_categoria,
                egreso.descripcion,
                egreso.fecha,
                egreso.id,
            )
            for egreso in egresos
        ]
