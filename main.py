from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from bcrypt import hashpw, gensalt, checkpw
import sqlite3
from sqlite3 import Error
import os
import secrets
from typing import List
from entidades import Usuario,Paciente,Consulta
from jwt import encode, decode
from datetime import datetime

app = FastAPI(
    docs_url="/"
)

c=os.getcwd()
ruta=c+'/datos.db'

jwtSecreto = "cdc556c0-bc6a-41bb-90e9-dd48f6082234" 

#-----Funciones Utilitarias
def encodePasword(password: str):
    #codificando contraseña
    return hashpw(password.encode("utf-8"), gensalt())

def checkPassword(password: str, hashPassword: str):
    #Valida que la contraseña de la db corresponda con la introducida por el usuario
    return checkpw(password.encode("utf-8"), hashPassword.encode("utf-8"))

def decodeToken(token: str):
    #Desencripta el token
    return decode(token, jwtSecreto)

def encodeToken(user: Usuario):
    #Crea el token
    exp = datetime.now().timestamp() + (60 * 60 * 1000)
    return encode({"exp": exp, "usuario": user}, jwtSecreto)
#--------------------------

#class Token(BaseModel):
#    access_token: str
#    token_type: str = "bearer"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

#--------------------User-----------------------
@app.post("/api/createUser", tags=["USER"])
def CreateUser(user:Usuario):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    nombre=user.Nombre
    email=user.Email   
    password = encodePasword(user.Clave)
   
    sql0 =F'SELECT Email FROM Usuario WHERE Email = "'+ email+'"'
    datos.execute(sql0)
    conexion.commit()
    informacion = datos.fetchall()
    if informacion == []:
        Info = (nombre,email,password)
        sql = f'INSERT INTO Usuario(Id, Nombre, Email, Clave) VALUES (NULL,?,?,?)'
        datos.execute(sql,Info)
        conexion.commit()
        return{'Welcome'}
    else:
        return{'Ya existe un correo con ese email'}
    
    
  
    

@app.post("/api/login",tags=["USER"] )
def Login(user:Usuario):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    email = user.Email
    password = user.Clave
       
    sql =F'SELECT Clave FROM Usuario WHERE Email = "'+ email+'"'
    datos.execute(sql)
    conexion.commit()
    informacion = datos.fetchall()
    for i in informacion:
        passwordR = checkPassword(password,i[0].decode())
        if passwordR == True:
                         
            return('Welcome')
        else:
            return('Contraseña Incorrecta')
    
 

@app.get("/api/info/{Id}", tags=["USER"])
def Info(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()
    
    query =f'SELECT Id, Nombre, Email, Clave FROM `Usuario` WHERE Id = {Id}'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
        
    return(informacion)


      

#-------------------Paciente--------------
@app.get("/api/patients", tags=["Patient"])
def Patients():
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    datos.execute('SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente')
    conexion.commit()
    informacion = datos.fetchall()
   
    return(informacion)

@app.post("/api/patients", tags=["Patient"])
def AddPatients(patient:Paciente):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    UsuarioId = patient.UsuarioId   
    Cedula = patient.Cedula 
    Foto = patient.Foto 
    Nombre = patient.Nombre 
    Apellido = patient.Apellido 
    TipoSangre = patient.TipoSangre 
    Email = patient.Email
    Sexo = patient.Sexo 
    FechaNacimiento = patient.FechaNacimiento 
    AlergiasId = 2
    SignoZodiacal = patient.SignoZodiacal
    
    sql0 =F'SELECT Cedula FROM Paciente WHERE Cedula = "'+ Cedula+'"'
    datos.execute(sql0)
    conexion.commit()
    informacion = datos.fetchall()
    if informacion == []:
        Info=(UsuarioId,Cedula,Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal)
        query = f'INSERT INTO Paciente(UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal)VALUES(?,?,?,?,?,?,?,?,?,?,?)'
        datos.execute(query,Info)
        conexion.commit()
        return{'Paciente Agregado'}
    else:
        return{'Ya existe un paciente con esa cedula'}


@app.get("/api/patients/{Id}", tags=["Patient"])
def FindPatient(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente WHERE Id = {Id};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return(informacion)




#----------------------Consults-----------------------
@app.post("/api/consults", tags=["Consult"])
def Consults(consults:Consulta):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    PacienteId = consults.PacienteId
    Fecha = consults.Fecha 
    Motivo = consults.Motivo 
    Seguro = consults.Seguro 
    MontoPagado = consults.MontoPagado 
    Diagnostico = consults.Diagnostico 
    Notas = consults.Notas
    Archivo = consults.Archivo

    Info = (PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo)
    query = f'INSERT INTO Consulta(PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo) VALUES (?,?,?,?,?,?,?,?);'
    datos.execute(query,Info)
    conexion.commit()
    return{'Consulta agregada'}


@app.get("/api/consults/{usuarioId}", tags=["Consult"])
def FindConsult(usuarioId:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM Consulta WHERE PacienteId = {usuarioId};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return(informacion)






