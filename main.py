from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from bcrypt import hashpw, gensalt, checkpw
import sqlite3
from sqlite3 import Error
import os
import secrets
from typing import List
from entidades import Usuario,Paciente,Consulta,UsuarioClave, Token
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
    return encode({"exp": exp, "usuario": {
        "Id": user.Id,
        "Nombre": user.Nombre,
        "Email": user.Email
    }}, jwtSecreto)
#--------------------------

#class Token(BaseModel):
#    access_token: str
#    token_type: str = "bearer"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

#--------------------User-----------------------
@app.post("/api/createUser", tags=["USER"])
def CreateUser(user:UsuarioClave):
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
        token = encodeToken(
            Usuario(
                Id = user.Id,
                Nombre=user.Nombre,
                Email = user.Email
                )
            )
        return {
            "status" : True, 
            "Token" : Token(access_token = token)
        }

    else:
        return{"message" : 'Ya existe un correo con ese email', "status": False}


@app.post("/api/login",tags=["USER"] )
def Login(user:UsuarioClave):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    email = user.Email
    password = user.Clave

    sql =F'SELECT Clave FROM Usuario WHERE Email = "'+ email+'"'
    datos.execute(sql)
    conexion.commit()
    informacion = datos.fetchall()
    for i in informacion:
        passwordR = checkPassword(password,i[0])
        if passwordR == True:
            token = encodeToken(
            Usuario(
                Id = user.Id,
                Nombre=user.Nombre,
                Email = user.Email
                ))

            return {
                "status" : True, 
                "Token" : Token(access_token = token)
            }
        else:
            return {
                "status": False,
                "message": 'Usuario o Contraseña Incorrecta'
            } 

@app.get("/api/info/{Id}", tags=["USER"])
def Info(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()
    
    query =f'SELECT Id, Nombre, Email, Clave FROM `Usuario` WHERE Id = {Id}'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
        
    return {
        "status" : True,
        "data" : (informacion)
    }


#-------------------Paciente--------------
@app.get("/api/patients", tags=["Patient"])
def Patients():
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    datos.execute('SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente')
    conexion.commit()
    informacion = datos.fetchall()

    return  {
        "status": True, 
        "data": informacion
    } 


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
    AlergiasId = patient.Alergias.Id
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
        return{
            "status" : True,
            "mensaje" : 'Paciente Agregado'
        }
    else:
        return{
            "status" : False,
            "mensaje" : 'Ya existe un paciente con esa cedula'
        }


@app.get("/api/patients/{Id}", tags=["Patient"])
def FindPatient(Id:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente WHERE Id = {Id};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return{
        "status" : True
        "data" : (informacion)
    }

@app.put("/api/patients/{idusuario}", tags=["Patient"])
def ModifyPatient(patient:Paciente,idusuario:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    idusuario0 = idusuario 

    UsuarioId = patient.UsuarioId   
    Cedula = patient.Cedula 
    Foto = patient.Foto 
    Nombre = patient.Nombre 
    Apellido = patient.Apellido 
    TipoSangre = patient.TipoSangre 
    Email = patient.Email
    Sexo = patient.Sexo 
    FechaNacimiento = patient.FechaNacimiento 
    AlergiasId = patient.Alergias.Id
    SignoZodiacal = patient.SignoZodiacal

    Info=(UsuarioId,Cedula,Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal,idusuario0)
    query = f'UPDATE Paciente SET UsuarioId = ?, Cedula = ?, Foto = ?, Nombre = ?, Apellido = ?, TipoSangre = ?, Email = ?, Sexo = ?, FechaNacimiento = ?, AlergiasId = ?, SignoZodiacal = ? WHERE Id = ? '
    datos.execute(query,Info)
    conexion.commit()
    return{
        "status" : True,
        f "mensaje" : 'Paciente Modificado, {Cedula}'
    }


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
    return{
        "status" : True,
        "mensaje" : 'Consulta agregada'
    }


@app.get("/api/consults/{usuarioid}", tags=["Consult"])
def FindConsult(usuarioid:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query =f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM Consulta WHERE PacienteId = {usuarioid};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    
    return {
        "status" : True,
        "data" : (informacion)
    }

@app.put("/api/consults/{idpaciente}", tags=["Consult"])
def ModifyConsult(consults:Consulta,idpaciente:int):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    PacienteId0 = idpaciente

    PacienteId = consults.PacienteId
    Fecha = consults.Fecha 
    Motivo = consults.Motivo 
    Seguro = consults.Seguro 
    MontoPagado = consults.MontoPagado 
    Diagnostico = consults.Diagnostico 
    Notas = consults.Notas
    Archivo = consults.Archivo

    # Info = (MontoPagado)
    Info = (PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo,PacienteId0)
    #query =f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM Consulta WHERE PacienteId = {PacienteId0}'
    
    #query = f"UPDATE Consulta SET PacienteId={PacienteId}, Fecha = {Fecha}, Seguro={Seguro},MontoPagado={MontoPagado},Diagnostico={Diagnostico},Notas={Notas},Archivo={Archivo} WHERE PacienteId = {PacienteId0}"
    
    #query = f'UPDATE Consulta SET PacienteId= "'+PacienteId+'", Fecha = "'+Fecha+'", Seguro="'+Seguro+'",MontoPagado="'+MontoPagado+'",Diagnostico="'+Diagnostico+'",Notas="'+Notas+'",Archivo="'+Archivo+'" WHERE PacienteId = "'+PacienteId0+'"'
    
    query = f'UPDATE Consulta SET PacienteId= ?, Fecha= ?, Motivo= ?, Seguro= ?, MontoPagado= ?, Diagnostico= ?, Notas= ?, Archivo= ? WHERE PacienteId = ? '
    #query = f'UPDATE Consulta SET PacienteId={PacienteId},Fecha={Fecha},Seguro={Seguro},MontoPagado={MontoPagado},Diagnostico={Diagnostico},Notas={Notas},Archivo={Archivo} WHERE PacienteId ={PacienteId0}'
    #query = UPDATE Consulta SET PacienteId=0, Fecha = '23/08/2019', Seguro='546546',MontoPagado=1000,Diagnostico='Algo malo',Notas='wao',Archivo='un archivo' WHERE PacienteId = 0
    # query = f'UPDATE Consulta SET  Seguro= "'+Seguro+'", Diagnostico= "'+Diagnostico+'", Notas= "'+Notas+'", Archivo= "'+Archivo+'"  '

    datos.execute(query,Info)
    conexion.commit()
    return{
        "status" : True,
        f "mensaje" : 'Datos modificados con éxito'
    }



#----------------------Resports-------------------
@app.get("/api/reports/{fecha}", tags=["Reports"])
def FindReport(fecha:str):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()

    query = f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM `Consulta` WHERE Fecha = "'+fecha+'" '
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()

    return {
        "status" : True,
        "data" : (informacion)
    }

@app.get("/api/reportss/{zodiaco}", tags=["Reports"])
def FindReportZ(zodiaco:str):
    conexion = sqlite3.connect(ruta)
    datos = conexion.cursor()
    zodiaco = zodiaco

    query = f'SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM `Paciente` WHERE SignoZodiacal = "'+zodiaco+'"'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    

    return {
        "status" : True,
        "data" : (informacion)
    }