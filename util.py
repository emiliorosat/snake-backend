from bcrypt import hashpw, gensalt, checkpw
from jwt import encode, decode
from datetime import datetime
from entidades import Usuario

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

def tokenTime(token:str, uid: int):
    NToken = decodeToken(token)
    tiempo = NToken['exp']
    if tiempo > datetime.now().timestamp() :
        return True if ( NToken["usuario"]["Id"] == uid) else False
    else:
        return{
        "status": False
        }