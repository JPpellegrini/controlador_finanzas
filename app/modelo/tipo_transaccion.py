from dataclasses import dataclass

from sqlalchemy import exc

from app.modelo.recursos import Session, TipoTransaccion


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
    def registrar_tipo(self, data: TipoTransaccionDTO):
        if data.nombre == "":
            raise NombreError
        session = Session()
        tipo = TipoTransaccion(
            id=data.id, nombre=data.nombre, descripcion=data.descripcion
        )
        session.add(tipo)
        session.commit()

    def editar_tipo(self, data: TipoTransaccionDTO):
        if data.nombre == "":
            raise NombreError
        session = Session()
        tipo = session.query(TipoTransaccion).filter_by(id=data.id).first()
        tipo.nombre = data.nombre
        tipo.descripcion = data.descripcion
        session.commit()

    def eliminar_tipo(self, data: TipoTransaccionDTO):
        try:
            session = Session()
            tipo = session.query(TipoTransaccion).filter_by(id=data.id).first()
            session.delete(tipo)
            session.commit()
        except exc.IntegrityError:
            raise TipoUsoError

    def obtener_tipos(self):
        session = Session()
        tipos = session.query(TipoTransaccion)
        return [
            TipoTransaccionDTO(tipo.nombre, tipo.descripcion, tipo.id) for tipo in tipos
        ]
