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
        return loginUser(user)

    else:
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
    return "bye"

"""
async def get_current_user(token:str = Depends(oauth2_scheme)):
    user = decodeToken(token)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Aunthenticate": "Bearer"},
        )
    return user
"""
#async def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
   #if current_user["user"]["Disabled"]:
    #    raise HTTPException(status_code=400, detail="Inactive user")
   # return current_user["user"] 

def userInfo(Id: int):
    conexion = db()
    datos = conexion.cursor()
    
    query =f'SELECT Id, Nombre, Email FROM `Usuario` WHERE Id = {Id}'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    data = []
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
    Clave = encodePasword(user.Clave)

    Info = (Nombre,Email,Clave,Id)
    query = f'Update Usuario SET Nombre= ?, Email= ?, Clave= ? WHERE Id = ? '
    datos.execute(query,Info)
    conexion.commit()
    
    return {
        "status" : True
    }


    