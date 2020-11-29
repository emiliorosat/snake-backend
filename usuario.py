import sqlite3
from sqlite3 import Error
from db import db
from entidades import UsuarioClave, Usuario, Token
from util import encodePasword, encode, checkPassword, encodeToken

#--------------------User-----------------------
def createNewUser(user:UsuarioClave):
    conexion = db()
    datos = conexion.cursor()

    nombre=user.Nombre
    email=user.Email   
    password = encodePasword(user.Clave)

    sql0 =f'SELECT Email FROM Usuario WHERE Email = "'+ email+'"'
    datos.execute(sql0)
    conexion.commit()
    informacion = datos.fetchall()
    if informacion == []:
        Info = (nombre,email,password)
        sql = f'INSERT INTO Usuario(Id, Nombre, Email, Clave) VALUES (NULL,?,?,?)'
        datos.execute(sql,Info)
        conexion.commit()
        conexion.close()
        return loginUser(user)

    else:
        conexion.close()
        return{"message" : 'Ya existe un correo con ese email', "status": False}


def loginUser(user:UsuarioClave):
    conexion = db()
    datos = conexion.cursor()

    email = user.Email
    password = user.Clave

    sql =f'SELECT Clave,Id,Nombre,Email FROM Usuario WHERE Email = "'+ email+'"'
    datos.execute(sql)
    conexion.commit()
    informacion = datos.fetchall()
    conexion.close()
    for i in informacion:
        passwordR = checkPassword(password,i[0].decode())
        if passwordR == True:
            token = encodeToken(
            Usuario(
                Id = i[1],
                Nombre=i[2],
                Email = i[3]
            ))

            return{
                
                "status" : True, 
                "Token" : Token(access_token = token),
                "Usuario" : {"Id" : i[1], "Nombre" : i[2]}
            }
        else:
            return {
                "status": False,
                "message": 'Usuario o Contraseña Incorrecta'
            } 
    return {
        "status": False,
        "message": 'Usuario No Existe'
    }


def userInfo(Id: int):
    conexion = db()
    datos = conexion.cursor()
    
    query =f'SELECT Id, Nombre, Email FROM `Usuario` WHERE Id = {Id}'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    data = []
    conexion.close()
    for i in informacion:
        data.append({
            "Id":i[0],
            "Nombre":i[1],
            "Email":i[2]
        })
        
    return {
        "status" : True,
        "data" : data
    }


def updateUser(user:UsuarioClave):
    conexion = db()
    datos = conexion.cursor()

    Id = user.Id
    Nombre = user.Nombre
    Email = user.Email

    if user.Clave != "" and user.Email != "":
        Clave = encodePasword(user.Clave)
        Info = (Nombre,Email,Clave,Id)
        query = f'Update Usuario SET Nombre= ?, Email= ?, Clave= ? WHERE Id = ? '
    elif user.Clave != "":
        Clave = encodePasword(user.Clave)
        Info = (Nombre,Clave,Id)
        query = f'Update Usuario SET Nombre= ?, Clave= ? WHERE Id = ? '
    elif user.Email != "":
        Info = (Nombre,Email,Id)
        query = f'Update Usuario SET Nombre= ?, Email= ? WHERE Id = ? '

    datos.execute(query,Info)
    conexion.commit()
    conexion.close()
    
    return {
        "status" : True
    }


    