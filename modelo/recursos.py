from os import getenv

import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


load_dotenv()
username = getenv("MYSQL_USERNAME")
password = getenv("MYSQL_PASSWORD")

engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/finanzas")

Session = sessionmaker(bind=engine)
Base = declarative_base()


class TipoTransaccion(Base):
    __tablename__ = "tipos_transaccion"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)


class CategoriaIngreso(Base):
    __tablename__ = "categorias_ingreso"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)


class CategoriaEgreso(Base):
    __tablename__ = "categorias_egreso"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)


class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True)
    monto = Column(String)
    id_tipo_transaccion = Column(
        Integer, ForeignKey("tipos_transaccion.id"), nullable=False
    )
    id_categoria = Column(Integer, ForeignKey("categorias_ingreso.id"), nullable=False)
    descripcion = Column(String)
    fecha = Column(DateTime)

    tipo_transaccion = relationship("TipoTransaccion", backref="ingresos")
    categoria = relationship("CategoriaIngreso", backref="ingresos")


class Egreso(Base):
    __tablename__ = "egresos"

    id = Column(Integer, primary_key=True)
    monto = Column(String)
    id_tipo_transaccion = Column(
        Integer, ForeignKey("tipos_transaccion.id"), nullable=False
    )
    id_categoria = Column(Integer, ForeignKey("categorias_egreso.id"), nullable=False)
    descripcion = Column(String)
    fecha = Column(DateTime)

    tipo_transaccion = relationship("TipoTransaccion", backref="egresos")
    categoria = relationship("CategoriaEgreso", backref="egresos")


class Database:
    __conexion = None

    @classmethod
    def get(cls, username=None, password=None):
        if not cls.__conexion:
            cls.__conexion = pymysql.connect(
                cursorclass=pymysql.cursors.DictCursor,
                host="localhost",
                port=3306,
                user=username,
                passwd=password,
                db="finanzas",
            )
        return cls.__conexion


class Balance:
    @staticmethod
    def calcular():
        database = Database.get()
        cursor = database.cursor()
        try:
            cursor.execute("SELECT SUM(monto) as total FROM ingresos")
            ingresos = cursor.fetchone()["total"]
            cursor.execute("SELECT SUM(monto) as total FROM egresos")
            egresos = cursor.fetchone()["total"]
            return ingresos - egresos
        except TypeError:
            if ingresos != None:
                return 0 + ingresos
            elif egresos != None:
                return 0 - egresos
            return 0
