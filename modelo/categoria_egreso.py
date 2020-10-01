from dataclasses import dataclass
from modelo.recursos import Session, CategoriaEgreso

from sqlalchemy import exc


@dataclass
class CategoriaEgresoDTO:
    nombre: str
    descripcion: str
    id: int = None


class NombreError(Exception):
    def __str__(self):
        return "Nombre invalido"


class CategoriaUsoError(Exception):
    def __str__(self):
        return "Error, categoria/s en uso"


class ServiceCategoriaEgreso:
    def registrar_cat_egreso(self, data: CategoriaEgresoDTO):
        if data.nombre == "":
            raise NombreError
        session = Session()
        categoria = CategoriaEgreso(
            id=data.id, nombre=data.nombre, descripcion=data.descripcion
        )
        session.add(categoria)
        session.commit()

    def editar_cat_egreso(self, data: CategoriaEgresoDTO):
        if data.nombre == "":
            raise NombreError
        session = Session()
        categoria = session.query(CategoriaEgreso).filter_by(id=data.id).first()
        categoria.nombre = data.nombre
        categoria.descripcion = data.descripcion
        session.commit()

    def eliminar_cat_egreso(self, data: CategoriaEgresoDTO):
        try:
            session = Session()
            categoria = session.query(CategoriaEgreso).filter_by(id=data.id).first()
            session.delete(categoria)
            session.commit()
        except exc.IntegrityError:
            raise CategoriaUsoError

    def obtener_cat_egreso(self):
        session = Session()
        categorias = session.query(CategoriaEgreso)
        return [
            CategoriaEgresoDTO(categoria.nombre, categoria.descripcion, categoria.id)
            for categoria in categorias
        ]
