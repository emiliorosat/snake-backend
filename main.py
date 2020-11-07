from fastapi import FastAPI
from typing import Optional
import sqlite3
from sqlite3 import Error
import os
import secrets
from typing import List
from entidades import Usuario
import bcrypt 
import jwt


app = FastAPI(
    docs_url="/"
)

c=os.getcwd()
ruta=c+'/datos.db'

''' User'''
@app.post("/API/CreateUser", tags=["USER"])
def CreateUser(user:Usuario):
    #try:    
    #    conexion = sqlite3.connect(ruta)
    #    datos = conexion.cursor()
    #    
    #
#
    #    datos.execute(f"INSERT INTO Usuario(Id,Nombre,Email,Clave) VALUES (NULL,{user.Nombre},{user.Email},{user.#clave}")
    #    conexion.commit()
    #    return{f'Registro Exitoso'}
    #except TypeError:
    #    return{"Hubo un error"}

    nombre=user.Nombre
    email=user.Email
    #clave=user.Clave
    clave = bcrypt.hashpw(user.Clave.encode("utf-8"),bcrypt.gensalt())
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    Info = (nombre,email,clave)
    sql = f'INSERT INTO Usuario(Id, Nombre, Email, Clave, Token) VALUES (NULL,?,?,?,NULL)'
    datos.execute(sql,Info)
    conexion.commit()


    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    
    

    return {"Registrado"}

@app.post("/API/Login",tags=["USER"] )
def Login(email:str,clave:str):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    

    token = secrets.token_hex(5)
    sql =F'UPDATE Usuario SET Token="'+token+'" WHERE Email= "'+email+'" AND Clave ="'+clave+'"'
    datos.execute(sql)
    conexion.commit()
    return{'Token',token,'Guardado'}
 

@app.get("/API/Info/{Id}", tags=["USER"])
def Info(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT Id, MedicoId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente WHERE Id = {Id};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return(informacion)


      

'''Paciente'''
@app.get("/API/Patients", tags=["Patient"])
def Patients():
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    datos.execute('SELECT Id, MedicoId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente')
    conexion.commit()
    informacion = datos.fetchall()


    
    return(informacion)

@app.post("/API/AddPatients", tags=["Patient"])
async def AddPatients(MedicoId:int,Cedula:str,Foto:str,Nombre:str,Apellido:str,TipoSangre:str,Email:str,Sexo:str,FechaNacimiento:str,AlergiasId:int,SignoZodiacal:str):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    
    Info=(MedicoId,Cedula,Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal)
    query = f'INSERT INTO Paciente(Id,MedicoId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal)VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)'
    datos.execute(query,Info)
    conexion.commit()
    return{'Registro exitoso'}



@app.get("/API/FindPatient/{Id}", tags=["Patient"])
def FindPatient(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT Id, MedicoId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente WHERE Id = {Id};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return(informacion)


@app.post("/API/AddConsults", tags=["Consult"])
def Consults(PacienteId:int, Fecha:str, Motivo:str, Seguro:str, MontoPagado:int, Diagnostico:str, Notas:str, Archivo:str):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    Info = (PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo)
    query = f'INSERT INTO Consulta(PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo) VALUES (?,?,?,?,?,?,?,?);'
    datos.execute(query,Info)
    conexion.commit()
    return{'Listo'}


@app.get("/API/FindConsults/{Id}", tags=["Consult"])
def FindConsult(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM Consulta WHERE PacienteId = {Id};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return(informacion)




