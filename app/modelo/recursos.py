from os import getenv

from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
)
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
    monto = Column(Float)
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
    monto = Column(Float)
    id_tipo_transaccion = Column(
        Integer, ForeignKey("tipos_transaccion.id"), nullable=False
    )
    id_categoria = Column(Integer, ForeignKey("categorias_egreso.id"), nullable=False)
    descripcion = Column(String)
    fecha = Column(DateTime)

    tipo_transaccion = relationship("TipoTransaccion", backref="egresos")
    categoria = relationship("CategoriaEgreso", backref="egresos")


class Balance:
    @staticmethod
    def calcular():
        session = Session()
        ingresos = session.query(func.sum(Ingreso.monto)).scalar()
        egresos = session.query(func.sum(Egreso.monto)).scalar()
        if not ingresos:
            ingresos = 0
        if not egresos:
            egresos = 0
        return round(ingresos - egresos, 2)
