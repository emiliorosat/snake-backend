from db import db
from entidades import Consulta


#----------------------Consults-----------------------
def addConsults(consults:Consulta, uid: int):
    conexion = db()
    datos = conexion.cursor()

    PacienteId = consults.PacienteId
    Fecha = consults.Fecha 
    Motivo = consults.Motivo 
    Seguro = consults.Seguro 
    MontoPagado = consults.MontoPagado 
    Diagnostico = consults.Diagnostico 
    Notas = consults.Notas
    Archivo = consults.Archivo

    Info = (PacienteId, uid, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo)
    query = f'INSERT INTO Consulta(PacienteId, UsuarioId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo) VALUES (?,?,?,?,?,?,?,?,?);'
    datos.execute(query,Info)
    conexion.commit()
    return{
        "status" : True,
        "mensaje" : 'Consulta agregada'
    }


def FindAllConsults(usuarioid:int):
    conexion = db()
    datos = conexion.cursor()

    query =f'SELECT c.PacienteId, c.Fecha, c.Motivo, c.Seguro, c.MontoPagado, c.Diagnostico, c.Notas, c.Archivo, p.Nombre, p.Apellido, c.Id FROM Consulta c INNER JOIN Paciente p ON c.PacienteId = p.Id WHERE c.UsuarioId = {usuarioid};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    data = []
    for i in informacion:
        data.append({
            "PacienteId" : i[0],
            "Fecha" : i[1],
            "Motivo": i[2],
            "Seguro": i[3],
            "MontoPagado":i[4],
            "Diagnostico":i[5],
            "Notas": i[6],
            "Archivo": i[7],
            "Nombre": i[8],
            "Apellido": i[9],
            "Id": i[10],
        }) 
    return {
        "status" : True,
        "data" : data,
        
    }

def FindConsultById(cid: int, uid: int):
    conexion = db()
    datos = conexion.cursor()
    query =f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM Consulta WHERE UsuarioId = {uid} AND Id={cid};'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    data = []
    for i in informacion:
        data.append({
            "PacienteId" : i[0],
            "Fecha" : i[1],
            "Motivo": i[2],
            "Seguro": i[3],
            "MontoPagado":i[4],
            "Diagnostico":i[5],
            "Notas": i[6],
            "Archivo": i[7]
        }) 
    return {
        "status" : True,
        "data" : data,
        
    }



def updateConsult(consults:Consulta,idpaciente:int):
    conexion = db()
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
    Info = (PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo,PacienteId0)
    query = f'UPDATE Consulta SET PacienteId= ?, Fecha= ?, Motivo= ?, Seguro= ?, MontoPagado= ?, Diagnostico= ?, Notas= ?, Archivo= ? WHERE PacienteId = ? '

    # Info = (MontoPagado)
    #query =f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM Consulta WHERE PacienteId = {PacienteId0}'
    
    #query = f"UPDATE Consulta SET PacienteId={PacienteId}, Fecha = {Fecha}, Seguro={Seguro},MontoPagado={MontoPagado},Diagnostico={Diagnostico},Notas={Notas},Archivo={Archivo} WHERE PacienteId = {PacienteId0}"
    
    #query = f'UPDATE Consulta SET PacienteId= "'+PacienteId+'", Fecha = "'+Fecha+'", Seguro="'+Seguro+'",MontoPagado="'+MontoPagado+'",Diagnostico="'+Diagnostico+'",Notas="'+Notas+'",Archivo="'+Archivo+'" WHERE PacienteId = "'+PacienteId0+'"'
    
    #query = f'UPDATE Consulta SET PacienteId={PacienteId},Fecha={Fecha},Seguro={Seguro},MontoPagado={MontoPagado},Diagnostico={Diagnostico},Notas={Notas},Archivo={Archivo} WHERE PacienteId ={PacienteId0}'
    #query = UPDATE Consulta SET PacienteId=0, Fecha = '23/08/2019', Seguro='546546',MontoPagado=1000,Diagnostico='Algo malo',Notas='wao',Archivo='un archivo' WHERE PacienteId = 0
    # query = f'UPDATE Consulta SET  Seguro= "'+Seguro+'", Diagnostico= "'+Diagnostico+'", Notas= "'+Notas+'", Archivo= "'+Archivo+'"  '

    datos.execute(query,Info)
    conexion.commit()
    return{
        f"status" : True,
        "mensaje" : 'Datos modificados con éxito'
    }
