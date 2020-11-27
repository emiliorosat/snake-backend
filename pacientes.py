from db import db
from entidades import Paciente
from zodiaco import ObrenerSigno


#-------------------Paciente--------------
def getAllPatients(uid: int):
    conexion = db()
    datos = conexion.cursor()

    datos.execute(f'SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente WHERE UsuarioId = {uid}')
    conexion.commit()
    informacion = datos.fetchall()
    data = builPatientsDic(informacion)
    conexion.close()
    
    return {
        "status": True,
        "data": data
    }

def builPatientsDic(data):
    nDic = []
    for i in data:
        nDic.append({
            "Id": i[0], "UsuarioId":i[1],"Cedula": i[2], "Foto": i[3], "Nombre": i[4], "Apellido": i[5],
            "TipoSangre": i[6], "Email": i[7], "Sexo": i[8], "FechaNacimiento": i[9], 
            "Alergias": i[10], "SignoZodiacal": i[11]

        })
    return nDic

def AddNewPatient(patient:Paciente):
    conexion = db()
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
    AlergiasId = ",".join( patient.Alergias )
    SignoZodiacal = ObrenerSigno(patient.FechaNacimiento)
    
    sql0 =f'SELECT Cedula FROM Paciente WHERE Cedula = "'+ Cedula+'"'
    datos.execute(sql0)
    conexion.commit()
    informacion = datos.fetchall()
    if informacion == []:
        Info=(UsuarioId,Cedula,Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal)
        query = f'INSERT INTO Paciente(UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal)VALUES(?,?,?,?,?,?,?,?,?,?,?)'
        datos.execute(query,Info)
        conexion.commit()
        conexion.close()
        return{
            "status" : True,
            "mensaje" : 'Paciente Agregado'
        }
    else:
        conexion.close()
        return{
            "status" : False,
            "mensaje" : 'Ya existe un paciente con esa cedula'
        }


def FindPatientInDb(Id:int):
    conexion = db()
    datos = conexion.cursor()

    query =f'SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM Paciente WHERE Id = {Id};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    data = builPatientsDic(informacion)
    conexion.close()
    return{
        "status" : True,
        "data" : data
    }

def updatePatient(patient:Paciente,idusuario:int):
    conexion = db()
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
    conexion.close()
    return{
        f"status" : True,
        "mensaje" : 'Paciente Modificado, {Cedula}'
    }

