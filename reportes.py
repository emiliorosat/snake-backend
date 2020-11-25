from db import db
from typing import Optional
from datetime import date
from entidades import Consulta, Paciente
from pacientes import builPatientsDic

"""
opciones:
1- Visitas por fecha, podrá seleccionar una fecha y saldrá los pacientes que visitaron en esa fecha.

2- Reporte zodiacal, aparecerá un listado de todos los pacientes cedula, nombre, apellido y signo zodiacal.

3- Reporte de pacientes con cantidad de visitas, aparecerá un listado con todos los pacientes registrados y al lado la cantidad de consultas que ha hecho ese paciente.


"""

#----------------------Resports-------------------
def FindAReport(opcion:int, uid: int, fecha: Optional[date]):
    if opcion == 1:
        sql = ""
    elif opcion == 2:
        sql= ""
    elif opcion == 3:
        sql = ""
    else:
        error = "Opcion Incorrecta"









"""
def algo():
    conexion = db()
    datos = conexion.cursor()

    if opcion==1 :
        query = f'SELECT PacienteId, Fecha, Motivo, Seguro, MontoPagado, Diagnostico, Notas, Archivo FROM `Consulta` WHERE Fecha = "'+fecha+'" '
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
    if opcion==2:
        zodiaco = ""
        return FindReportZ(zodiaco)
        

def FindReportZ(zodiaco:str):
    conexion = db()
    datos = conexion.cursor()
    zodiaco = zodiaco

    query = f'SELECT Id, UsuarioId, Cedula, Foto, Nombre, Apellido, TipoSangre, Email, Sexo, FechaNacimiento, AlergiasId, SignoZodiacal FROM `Paciente` WHERE SignoZodiacal = "'+zodiaco+'"'
    datos.execute(query)
    conexion.commit()
    informacion = datos.fetchall()
    data = builPatientsDic(informacion)
    

    return {
        "status" : True,
        "data" : data
    }

"""