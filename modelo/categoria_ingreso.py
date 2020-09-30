from dataclasses import dataclass
from modelo.recursos import Session, CategoriaIngreso

from sqlalchemy import exc


@dataclass
class CategoriaIngresoDTO:
    nombre: str
    descripcion: str
    id: int = None


class NombreError(Exception):
    def __str__(self):
        return "Nombre invalido"


class CategoriaUsoError(Exception):
    def __str__(self):
        return "Error, categoria/s en uso"


class ServiceCategoriaIngreso:
    def registrar_cat_ingreso(self, data: CategoriaIngresoDTO):
        if data.nombre == "":
            raise NombreError
        session = Session()
        categoria = CategoriaIngreso(
            id=data.id, nombre=data.nombre, descripcion=data.descripcion
        )
        session.add(categoria)
        session.commit()

    def editar_cat_ingreso(self, data: CategoriaIngresoDTO):
        if data.nombre == "":
            raise NombreError
        session = Session()
        categoria = session.query(CategoriaIngreso).filter_by(id=data.id).first()
        categoria.nombre = data.nombre
        categoria.descripcion = data.descripcion
        session.commit()

    def eliminar_cat_ingreso(self, data: CategoriaIngresoDTO):
        try:
            session = Session()
            categoria = session.query(CategoriaIngreso).filter_by(id=data.id).first()
            session.delete(categoria)
            session.commit()
        except exc.IntegrityError:
            raise CategoriaUsoError

    def obtener_cat_ingreso(self):
        session = Session()
        categorias = session.query(CategoriaIngreso)
        return [
            CategoriaIngresoDTO(categoria.nombre, categoria.descripcion, categoria.id)
            for categoria in categorias
        ]
