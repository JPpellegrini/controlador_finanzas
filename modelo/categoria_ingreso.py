from dataclasses import dataclass
from modelo.recursos import Database


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
    def __init__(self):
        self.database = Database.get()
        self.cursor = self.database.cursor()

    def registrar_cat_ingreso(self, data: CategoriaIngresoDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "INSERT INTO categorias_ingreso (id, nombre, descripcion) VALUES (%s, %s, %s)",
            (data.id, data.nombre, data.descripcion),
        )
        self.database.commit()

    def editar_cat_ingreso(self, data: CategoriaIngresoDTO):
        if data.nombre == "":
            raise NombreError
        self.cursor.execute(
            "UPDATE categorias_ingreso SET nombre=%s, descripcion=%s WHERE id = %s",
            (data.nombre, data.descripcion, data.id),
        )
        self.database.commit()

    def eliminar_cat_ingreso(self, data: CategoriaIngresoDTO):
        try:
            self.cursor.execute("DELETE FROM categorias_ingreso WHERE id = %s", data.id)
            self.database.commit()
        except pymysql.Error:
            raise CategoriaUsoError

    def obtener_cat_ingreso(self):
        self.cursor.execute("SELECT id, nombre, descripcion FROM categorias_ingreso")
        return [
            CategoriaIngresoDTO(
                categoria["nombre"], categoria["descripcion"], categoria["id"]
            )
            for categoria in self.cursor.fetchall()
        ]
