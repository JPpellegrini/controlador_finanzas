import os

import pymysql
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
username = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")

engine = create_engine(f"mysql+pymysql://{username}:{password}@localhost/finanzas")

Session = sessionmaker(bind=engine)

Base = declarative_base()


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
