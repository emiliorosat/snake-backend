import os
import sqlite3
from sqlite3 import Error

c=os.getcwd()
#ruta=c+'/datos.db'


def db():
    return sqlite3.connect("./datos.db")

def aplicandoMigracion():
    schema = open("./SQLite.sql", "r")
    cadena = schema.readlines()
    migration = "".join(cadena)
    schema.close()
    conexion = db()
    query = conexion.cursor()
    query.executescript(migration)
    conexion.close()

aplicandoMigracion()