import pymysql


class Database:
    __conexion = None

    @classmethod
    def get(cls, username = None, password = None): 
        if not cls.__conexion:  
            cls.__conexion = pymysql.connect(cursorclass=pymysql.cursors.DictCursor,host="localhost",
                                            port=3306, user=username, passwd=password, db="finanzas")
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