from dataclasses import dataclass
import pymysql


@dataclass
class TransaccionDTO:
    monto: float
    id_movimiento: int
    id_categoria: int
    descripcion: str
    fecha: str

@dataclass
class MovimientoDTO:
    nombre: str
    descripcion: str

@dataclass
class CategoriaDTO:
    nombre: str
    descripcion: str


class Service:
    def __init__(self):
        self.conexion = pymysql.connect(host="localhost", port=3306, user="usuario",
                                        passwd="1234", db="finanzas")
        self.cursor = self.conexion.cursor()

    def buscar(self, tabla, campo = None, condicion = None, valor = None):
        if campo:
            self.cursor.execute(
                "SELECT * FROM {} WHERE {} {} %s".format(tabla, campo, condicion), (valor)
            )
        else:
            self.cursor.execute(
                "SELECT * FROM {}".format(tabla)
            )
        return self.cursor.fetchall()

    def eliminar(self, tabla, id):
        self.cursor.execute(
            "DELETE FROM {} WHERE id = %s".format(tabla), (id)
        )
        self.conexion.commit()

    def editar(self, tabla, campo, valor):
        self.cursor.execute(
            "UPDATE {} SET {} = %s".format(tabla, campo), (valor)
        )
        self.conexion.commit()

    def registrar_movimiento(self, data = MovimientoDTO):
        self.cursor.execute(
            "INSERT INTO movimientos VALUES (%s, %s, %s)", (None, data.nombre, data.descripcion)
        )
        self.conexion.commit()
        
    def registrar_categoria(self, tipo, data = CategoriaDTO):
        self.cursor.execute(
            "INSERT INTO {} VALUES (%s, %s, %s)".format(tipo), (None, data.nombre, data.descripcion)
        )
        self.conexion.commit()

    def registrar_transaccion(self, tipo, data = TransaccionDTO):
        self.cursor.execute(
            "INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s)".format(tipo), (None, data.monto, data.id_movimiento,
                                                                            data.id_categoria, data.descripcion, data.fecha,)
        )
        self.conexion.commit()

    def calcular_balance(self):
        balance = 0
        for ingreso in self.buscar("ingresos"):
            balance += ingreso[1]
        for egreso in self.buscar("egresos"):
            balance -= egreso[1]
        return balance

    def cerrar_database(self):
        self.conexion.close()

if __name__ == "__main__":
    transaccion = TransaccionDTO(0.50, 1, 1, "", "2019")
    modelo = Service()
    
    print(modelo.calcular_valance())
    modelo.cerrar_database()